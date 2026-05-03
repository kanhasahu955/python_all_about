import argparse

import uvicorn

from app.settings import settings


def main() -> None:
    parser = argparse.ArgumentParser(description="MJPEG + OpenCV stream server")
    parser.add_argument("--host", default=settings.host, help="Bind host")
    parser.add_argument("--port", type=int, default=settings.port, help="Bind port")
    parser.add_argument("--reload", action="store_true", help="Dev reload")
    args = parser.parse_args()
    uvicorn.run(
        "app.main:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
    )


if __name__ == "__main__":
    main()
