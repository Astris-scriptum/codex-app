from __future__ import annotations
import argparse, json, sys, threading, webbrowser
from dataclasses import asdict
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parents[4]
for path in (REPO_ROOT / "packages" / "shared", REPO_ROOT / "packages" / "engine"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from codex_engine import EngineService
from codex_engine.workspace import CandidateRepository

class StudioApplication:
    def __init__(self, workspace_root: Path | None = None) -> None:
        self.workspace_root = workspace_root or (REPO_ROOT / "state" / "studio")
        self.workspace_root.mkdir(parents=True, exist_ok=True)
        self.engine = EngineService()
        self.repository = CandidateRepository(self.workspace_root / "candidates.jsonl")

    def health(self) -> dict:
        return {"status": "ok", "product": "Codex Studio", "engine": self.engine.statistics()}

    def discover(self, payload: dict) -> dict:
        source_text = str(payload.get("source_text", "")).strip()
        language = str(payload.get("language", "latin")).strip() or "latin"
        if not source_text:
            raise ValueError("source_text is required")
        candidates = self.engine.discover(source_text, language=language)
        return {
            "source_text": source_text,
            "language": language,
            "candidate_count": len(candidates),
            "candidates": [asdict(c) for c in candidates],
        }

    def save_candidate(self, payload: dict) -> dict:
        source_text = str(payload.get("source_text", "")).strip()
        candidate_text = str(payload.get("candidate_text", "")).strip()
        if not source_text or not candidate_text:
            raise ValueError("source_text and candidate_text are required")
        match = next((c for c in self.engine.discover(source_text) if c.text == candidate_text), None)
        if match is None:
            raise ValueError("candidate not found for source text")
        self.repository.append(match)
        return {"saved": True, "candidate_id": match.candidate_id, "text": match.text}

    def history(self) -> dict:
        rows = self.repository.read_all()
        return {"count": len(rows), "items": rows}

class Handler(BaseHTTPRequestHandler):
    app: StudioApplication
    static_root: Path

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/health":
            return self._json(HTTPStatus.OK, self.app.health())
        if path == "/api/history":
            return self._json(HTTPStatus.OK, self.app.history())
        self._static(path)

    def do_POST(self):
        path = urlparse(self.path).path
        try:
            payload = self._read_json()
            if path == "/api/discover":
                return self._json(HTTPStatus.OK, self.app.discover(payload))
            if path == "/api/save":
                return self._json(HTTPStatus.OK, self.app.save_candidate(payload))
            self._json(HTTPStatus.NOT_FOUND, {"error": "not found"})
        except ValueError as exc:
            self._json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
        except Exception as exc:
            self._json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": str(exc)})

    def log_message(self, fmt, *args):
        return

    def _read_json(self):
        raw = self.rfile.read(int(self.headers.get("Content-Length", "0") or "0")) or b"{}"
        value = json.loads(raw.decode("utf-8"))
        if not isinstance(value, dict):
            raise ValueError("JSON body must be an object")
        return value

    def _json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False, default=str).encode("utf-8")
        self.send_response(status.value)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _static(self, path):
        relative = "index.html" if path in ("", "/") else path.lstrip("/")
        target = (self.static_root / relative).resolve()
        root = self.static_root.resolve()
        if root not in target.parents and target != root:
            return self.send_error(HTTPStatus.FORBIDDEN)
        if not target.exists() or not target.is_file():
            target = root / "index.html"
        mime = {".html":"text/html; charset=utf-8",".css":"text/css; charset=utf-8",".js":"application/javascript; charset=utf-8"}.get(target.suffix,"application/octet-stream")
        data = target.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

class CodexStudioServer:
    def __init__(self, host="127.0.0.1", port=8765):
        static_root = Path(__file__).resolve().parent / "static"
        app = StudioApplication()
        handler = type("ConfiguredHandler", (Handler,), {"app": app, "static_root": static_root})
        self.host, self.port = host, port
        self.httpd = ThreadingHTTPServer((host, port), handler)

    def serve_forever(self, open_browser=True):
        url = f"http://{self.host}:{self.port}"
        if open_browser:
            threading.Timer(0.5, lambda: webbrowser.open(url)).start()
        print(f"Codex Studio running at {url}")
        print("Press Control-C to stop.")
        try:
            self.httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.httpd.server_close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()
    CodexStudioServer(args.host, args.port).serve_forever(not args.no_browser)

if __name__ == "__main__":
    main()
