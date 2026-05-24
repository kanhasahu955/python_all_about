from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def resolve_resume_path(file_path: str) -> Path | None:
    if not file_path:
        return None

    name = Path(file_path).name
    candidates = [
        Path(file_path),
        PROJECT_ROOT / file_path,
        PROJECT_ROOT / "storage" / "resumes" / name,
    ]

    for candidate in candidates:
        try:
            resolved = candidate.resolve()
            if resolved.is_file():
                return resolved
        except OSError:
            continue
    return None
