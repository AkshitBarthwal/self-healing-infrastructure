
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import docker
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("self-healing")
client = docker.from_env()

TARGET_CONTAINER = "nginx"
COOLDOWN_SECONDS = 60
last_restart = 0


class WebhookHandler(BaseHTTPRequestHandler):

    def send_json(self, status_code, data):
        body = json.dumps(data).encode()
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        import hmac

        auth_header = self.headers.get("Authorization", "")

        try:
            with open("/run/secrets/webhook_token", "r") as f:
                expected_token = f.read().strip()
        except OSError:
            logger.error("Webhook token file unavailable")
            self.send_json(500, {"error": "Server configuration error"})
            return

        expected_header = f"Bearer {expected_token}"

        if not hmac.compare_digest(auth_header, expected_header):
            self.send_json(401, {"error": "Unauthorized"})
            return

        global last_restart

        if self.path != "/alerts":
            self.send_json(404, {"error": "Not found"})
            return

        length = int(self.headers.get("Content-Length", 0))

        try:
            payload = json.loads(self.rfile.read(length))
        except (json.JSONDecodeError, ValueError):
            self.send_json(400, {"error": "Invalid JSON"})
            return

        status = payload.get("status")
        logger.info("Alert received | status=%s", status)

        if status != "firing":
            self.send_json(200, {
                "message": "No action required",
                "status": status
            })
            return

        alerts = payload.get("alerts", [])

        should_restart = any(
            alert.get("labels", {}).get("alertname") == "NginxServiceDown"
            and alert.get("status") == "firing"
            for alert in alerts
        )

        if not should_restart:
            self.send_json(200, {
                "message": "No matching recovery rule"
            })
            return

        now = time.time()

        if now - last_restart < COOLDOWN_SECONDS:
            self.send_json(200, {
                "message": "Restart skipped: cooldown active"
            })
            return

        try:
            container = client.containers.get(TARGET_CONTAINER)

            logger.info("Recovery started | container=%s", TARGET_CONTAINER)

            container.restart(timeout=10)
            last_restart = time.time()

            logger.info("Recovery completed | action=restart")

            self.send_json(200, {
                "message": "NGINX restart triggered",
                "container": TARGET_CONTAINER
            })

        except Exception:
            logger.exception("Recovery failed")
            self.send_json(500, {"error": "Recovery failed"})

    def log_message(self, fmt, *args):
        logger.info(fmt, *args)


server = HTTPServer(("0.0.0.0", 5001), WebhookHandler)
logger.info("Self-healing webhook listening on port 5001")
server.serve_forever()
