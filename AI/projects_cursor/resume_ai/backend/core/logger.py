"""
Centralized application logging: structured file logs + rich console output.
Call ``configure_logging()`` once at process startup (e.g. in ``main.py``).
"""

from __future__ import annotations

import logging
import sys
import warnings
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.config import Settings

_configured = False

# File logs: full context for grep / log aggregation
_FILE_FORMAT = (
    "%(asctime)s | %(levelname)-8s | %(name)s | "
    "%(filename)s:%(lineno)d | %(message)s"
)
_FILE_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def _ensure_log_dir(log_file: str | Path) -> Path:
    path = Path(log_file).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _root_level_from_settings(settings: Settings) -> int:
    if settings.DEBUG or settings.APP_ENV.lower() in ("dev", "development", "local"):
        return logging.DEBUG
    return logging.INFO


def configure_logging(settings: Settings | None = None) -> None:
    """
    Attach handlers to the root logger. Safe to call once per process; repeats are no-ops.
    """
    global _configured
    if _configured:
        return

    if settings is None:
        from core.config import get_settings

        settings = get_settings()

    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(_root_level_from_settings(settings))

    log_path = _ensure_log_dir(settings.LOG_FILE)

    # --- Console: Rich when available, else plain StreamHandler ---
    try:
        from rich.console import Console
        from rich.logging import RichHandler
        from rich.traceback import install as rich_install_traceback

        rich_install_traceback(show_locals=settings.DEBUG, suppress=[])

        console = Console(stderr=True, width=None, soft_wrap=True)
        console_handler: logging.Handler = RichHandler(
            console=console,
            show_time=True,
            show_path=False,
            markup=False,
            rich_tracebacks=True,
            tracebacks_show_locals=settings.DEBUG,
            keywords=[],
        )
        # RichHandler uses its own layout; keep message as record.getMessage()
        console_handler.setFormatter(logging.Formatter("%(message)s"))
    except ImportError:
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
                datefmt=_FILE_DATE_FORMAT,
            )
        )

    console_handler.setLevel(_root_level_from_settings(settings))

    # --- File: rotating, detailed ---
    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter(_FILE_FORMAT, datefmt=_FILE_DATE_FORMAT)
    )

    root.addHandler(console_handler)
    root.addHandler(file_handler)

    # Route warnings through logging
    logging.captureWarnings(True)

    # Quiet overly chatty libraries outside debug
    if not settings.DEBUG:
        for name, level in (
            ("urllib3", logging.WARNING),
            ("sqlalchemy.engine", logging.WARNING),
        ):
            logging.getLogger(name).setLevel(level)

    _configured = True
    logging.getLogger(__name__).debug(
        "Logging configured | env=%s | file=%s",
        settings.APP_ENV,
        log_path,
    )


def get_logger(name: str) -> logging.Logger:
    """Return a module-level logger (child of root)."""
    return logging.getLogger(name)
