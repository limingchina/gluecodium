#!/usr/bin/env python3
"""Serve the calculator browser example with Emscripten's required headers."""

import argparse
import functools
import mimetypes
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


class CalculatorRequestHandler(SimpleHTTPRequestHandler):
    """Static file handler configured for the pthread-enabled wasm module."""

    extensions_map = {
        **mimetypes.types_map,
        ".mjs": "text/javascript",
        ".wasm": "application/wasm",
    }

    def end_headers(self):
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        super().end_headers()


def parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--directory",
        type=Path,
        default=Path(__file__).absolute().parent,
        help="directory containing index.html and the generated module",
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    return parser.parse_args()


def main():
    arguments = parse_arguments()
    directory = arguments.directory.expanduser().resolve()
    handler = functools.partial(CalculatorRequestHandler, directory=str(directory))
    server = ThreadingHTTPServer((arguments.host, arguments.port), handler)
    print(f"Serving {directory} at http://{arguments.host}:{arguments.port}/index.html")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
