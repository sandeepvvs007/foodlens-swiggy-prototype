from __future__ import annotations

import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from agent_graph import run_foodlens_agent
from analyzer import analyze_orders


ROOT = Path(__file__).resolve().parent
STATIC_DIR = ROOT / "static"
DATA_PATH = ROOT / "data" / "mock_orders.json"


class PrototypeHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/analysis":
            query = parse_qs(parsed.query)
            self._send_analysis(query)
            return
        if parsed.path == "/health":
            self._send_json({"ok": True})
            return
        super().do_GET()

    def _send_analysis(self, query: dict):
        period_days = self._to_int(query.get("period", ["30"])[0], 30)
        monthly_budget = self._to_int(query.get("budget", ["6000"])[0], 6000)
        with DATA_PATH.open("r", encoding="utf-8") as file:
            orders = json.load(file)
        analysis = analyze_orders(orders, period_days, monthly_budget)
        agent_output = run_foodlens_agent(analysis)
        self._send_json({**analysis, **agent_output})

    def _to_int(self, value: str, default: int) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    def _send_json(self, payload: dict):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main():
    server = ThreadingHTTPServer(("127.0.0.1", 8000), PrototypeHandler)
    print("Swiggy Food Insights prototype running at http://127.0.0.1:8000")
    print("OAuth callback placeholder: http://localhost:8000/auth/callback")
    server.serve_forever()


if __name__ == "__main__":
    main()
