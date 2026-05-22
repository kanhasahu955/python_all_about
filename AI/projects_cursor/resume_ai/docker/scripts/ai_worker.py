"""Lightweight AI-sidecar: health HTTP + placeholder for batch/embed jobs (PM2 / Compose)."""

from __future__ import annotations

import json
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("ai-worker")


class _Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args: object) -> None:
        log.info("%s - %s", self.address_string(), fmt % args)

    def do_GET(self) -> None:
        if self.path in ("/", "/health"):
            body = json.dumps({"status": "ok", "service": "resume-ai-ai-worker"}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        self.send_response(404)
        self.end_headers()


def main() -> None:
    host, port = "0.0.0.0", 8765
    log.info("listening on %s:%s", host, port)
    HTTPServer((host, port), _Handler).serve_forever()


if __name__ == "__main__":
    main()
