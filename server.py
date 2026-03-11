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
import mimetypes
import re
from datetime import datetime

PORT = 8765
BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "data.json"
HTML_FILE = BASE_DIR / "index.html"
BERITA_DIR = BASE_DIR / "berita-acara"
GAMBAR_DIR = BASE_DIR / "gambar-asset"

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
        clean_path = self.path.split("?", 1)[0]
        if clean_path in ("/", "/index.html"):
            self._serve_file(HTML_FILE, "text/html")
        elif clean_path in ("/api/data", "/api/data/"):
            if DATA_FILE.exists():
                data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            else:
                data = {}
            self.send_json(200, {"ok": True, "data": data})
        else:
            # Serve static files from the app folder (e.g. logo.png).
            rel = clean_path.lstrip("/")
            target = (BASE_DIR / rel).resolve()
            if rel and str(target).startswith(str(BASE_DIR.resolve())) and target.is_file():
                mime = mimetypes.guess_type(str(target))[0] or "application/octet-stream"
                self._serve_file(target, mime)
                return
            self.send_json(404, {"ok": False, "error": "Not found"})

    def do_POST(self):
        clean_path = self.path.split("?", 1)[0]
        if clean_path in ("/api/data", "/api/data/"):
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            try:
                payload = json.loads(body)
                DATA_FILE.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
                self.send_json(200, {"ok": True})
                print(f"  ✅ data.json saved ({DATA_FILE.stat().st_size} bytes)")
            except Exception as e:
                self.send_json(500, {"ok": False, "error": str(e)})
        elif clean_path in ("/api/upload-berita-acara", "/api/upload-berita-acara/"):
            self._handle_upload_berita_acara()
        elif clean_path in ("/api/upload-gambar-asset", "/api/upload-gambar-asset/"):
            self._handle_upload_gambar_asset()
        elif clean_path in ("/api/delete-file", "/api/delete-file/"):
            self._handle_delete_file()
        else:
            self.send_json(404, {"ok": False, "error": "Not found"})

    def _handle_upload_berita_acara(self):
        self._handle_upload_file(BERITA_DIR, "berita_acara")

    def _handle_upload_gambar_asset(self):
        self._handle_upload_file(GAMBAR_DIR, "gambar_asset")

    def _handle_upload_file(self, target_dir: Path, fallback_stem: str):
        try:
            ctype = self.headers.get("Content-Type", "")
            if "multipart/form-data" not in ctype:
                self.send_json(400, {"ok": False, "error": "Invalid content type"})
                return

            m = re.search(r'boundary=([^;]+)', ctype)
            if not m:
                self.send_json(400, {"ok": False, "error": "Missing multipart boundary"})
                return
            boundary = m.group(1).strip().strip('"')

            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0:
                self.send_json(400, {"ok": False, "error": "Empty upload body"})
                return

            raw_body = self.rfile.read(length)
            boundary_bytes = ("--" + boundary).encode("utf-8")
            parts = raw_body.split(boundary_bytes)

            file_bytes = None
            original_name = None
            for part in parts:
                part = part.strip(b"\r\n")
                if not part or part == b"--":
                    continue
                if part.endswith(b"--"):
                    part = part[:-2]
                header_blob, sep, data_blob = part.partition(b"\r\n\r\n")
                if not sep:
                    continue
                headers_text = header_blob.decode("latin-1", errors="ignore")
                disp = re.search(r'Content-Disposition:\s*form-data;\s*name="([^"]+)"(?:;\s*filename="([^"]*)")?', headers_text, re.IGNORECASE)
                if not disp:
                    continue
                field_name = disp.group(1)
                filename = disp.group(2) or ""
                if field_name != "file":
                    continue
                if not filename:
                    continue
                file_bytes = data_blob.rstrip(b"\r\n")
                original_name = Path(filename).name
                break

            if file_bytes is None or original_name is None:
                self.send_json(400, {"ok": False, "error": "File field is required"})
                return

            if not original_name:
                self.send_json(400, {"ok": False, "error": "No file selected"})
                return

            stem = Path(original_name).stem
            ext = Path(original_name).suffix.lower()
            safe_stem = re.sub(r"[^A-Za-z0-9_-]+", "_", stem).strip("_") or fallback_stem
            if len(ext) > 10:
                ext = ""

            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            generated_name = f"{safe_stem}_{ts}{ext}"

            target_dir.mkdir(parents=True, exist_ok=True)
            target = target_dir / generated_name
            idx = 1
            while target.exists():
                generated_name = f"{safe_stem}_{ts}_{idx}{ext}"
                target = target_dir / generated_name
                idx += 1

            target.write_bytes(file_bytes)

            self.send_json(200, {
                "ok": True,
                "filename": generated_name,
                "original_name": original_name
            })
        except Exception as e:
            self.send_json(500, {"ok": False, "error": str(e)})

    def _handle_delete_file(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            payload = json.loads(body or b"{}")
            file_type = (payload.get("type") or "").strip().lower()
            filename = Path(payload.get("filename") or "").name

            if not filename:
                self.send_json(400, {"ok": False, "error": "filename is required"})
                return

            if file_type == "berita_acara":
                base_dir = BERITA_DIR
            elif file_type == "gambar_asset":
                base_dir = GAMBAR_DIR
            else:
                self.send_json(400, {"ok": False, "error": "Invalid file type"})
                return

            target = (base_dir / filename).resolve()
            if not str(target).startswith(str(base_dir.resolve())):
                self.send_json(400, {"ok": False, "error": "Invalid path"})
                return

            if target.exists() and target.is_file():
                target.unlink()
                self.send_json(200, {"ok": True, "deleted": True})
                return

            # Treat missing file as success so delete flow remains smooth.
            self.send_json(200, {"ok": True, "deleted": False})
        except Exception as e:
            self.send_json(500, {"ok": False, "error": str(e)})

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
