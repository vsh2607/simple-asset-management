#!/usr/bin/env python3
"""
AssetTrack Local Server
Run this script, then open http://localhost:8765 in your browser.
All data is saved to data.json in the same folder.
"""

import http.server
import json
import os
import sys
from pathlib import Path

PORT = 8765
BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "data.json"
HTML_FILE = BASE_DIR / "index.html"

class Handler(http.server.BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        print(f"  {args[0]} {args[1]}")

    def send_json(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self._serve_file(HTML_FILE, "text/html")
        elif self.path == "/api/data":
            if DATA_FILE.exists():
                data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            else:
                data = {}
            self.send_json(200, {"ok": True, "data": data})
        else:
            self.send_json(404, {"ok": False, "error": "Not found"})

    def do_POST(self):
        if self.path == "/api/data":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            try:
                payload = json.loads(body)
                DATA_FILE.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
                self.send_json(200, {"ok": True})
                print(f"  ✅ data.json saved ({DATA_FILE.stat().st_size} bytes)")
            except Exception as e:
                self.send_json(500, {"ok": False, "error": str(e)})
        else:
            self.send_json(404, {"ok": False, "error": "Not found"})

    def _serve_file(self, path, mime):
        if not path.exists():
            self.send_json(404, {"error": f"{path.name} not found"})
            return
        content = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", len(content))
        self.end_headers()
        self.wfile.write(content)


if __name__ == "__main__":
    print("=" * 50)
    print("  AssetTrack Local Server")
    print("=" * 50)
    print(f"  Folder : {BASE_DIR}")
    print(f"  Data   : {DATA_FILE}")
    print(f"  URL    : http://localhost:{PORT}")
    print()
    print("  Open your browser at: http://localhost:8765")
    print("  Press Ctrl+C to stop.")
    print("=" * 50)

    server = http.server.HTTPServer(("localhost", PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped.")
