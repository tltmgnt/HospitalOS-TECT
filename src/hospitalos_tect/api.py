"""Loopback-only synthetic-data assurance API; NOT for clinical use."""
from dataclasses import asdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from .assurance import Claim, Evidence, Rule, assess
from .security import authenticate, permitted


class Handler(BaseHTTPRequestHandler):
    def _respond(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            return self._respond(200, {"status": "ok", "mode": "synthetic-prototype"})
        self._respond(404, {"error": "not_found"})

    def do_POST(self):
        if self.path != "/v1/assess":
            return self._respond(404, {"error": "not_found"})
        principal = authenticate(self.headers.get("Authorization"))
        if principal is None:
            return self._respond(401, {"error": "unauthorized"})
        tenant_id = self.headers.get("X-Tenant-ID", "")
        if not permitted(principal, tenant_id, "assurance:assess"):
            return self._respond(403, {"error": "forbidden"})
        if self.headers.get("Content-Type", "").split(";")[0].strip().lower() != "application/json":
            return self._respond(415, {"error": "unsupported_media_type"})
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 65536:
                return self._respond(413, {"error": "invalid_size"})
            data = json.loads(self.rfile.read(length))
            claim_data = data["claim"]
            claim = Claim(
                id=claim_data["id"], text=claim_data["text"],
                evidence_ids=tuple(claim_data["evidence_ids"]),
            )
            evidence = [Evidence(**item) for item in data["evidence"]]
            rules = [Rule(**item) for item in data["rules"]]
            result = assess(claim, evidence, rules)
        except (ValueError, TypeError, KeyError, json.JSONDecodeError):
            return self._respond(400, {"error": "invalid_request"})
        self._respond(200, asdict(result))


if __name__ == "__main__":
    print("LOCAL PROTOTYPE ONLY: never submit patient information.")
    ThreadingHTTPServer(("127.0.0.1", 8080), Handler).serve_forever()
