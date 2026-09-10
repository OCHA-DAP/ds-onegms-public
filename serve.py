"""No-cache static server for local preview of index.html.

The page is a single file with inline CSS and JS, so a cached copy is stale in
every respect. Every response therefore carries no-store headers.

Usage:  python3 serve.py [port]      (default 8770)   ->  http://127.0.0.1:8770/
"""
import http.server
import os
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8770
HERE = os.path.dirname(os.path.abspath(__file__))


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=HERE, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()


if __name__ == "__main__":
    with http.server.ThreadingHTTPServer(("127.0.0.1", PORT), NoCacheHandler) as httpd:
        print(f"Serving {HERE} at http://127.0.0.1:{PORT}/  (Ctrl-C to stop)")
        httpd.serve_forever()
