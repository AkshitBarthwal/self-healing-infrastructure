from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        try:
            payload = json.loads(body)
            print("Alert received:", json.dumps(payload, indent=2), flush=True)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Alert received successfully")

        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid JSON")

    def log_message(self, format, *args):
        print(format % args, flush=True)


server = HTTPServer(("0.0.0.0", 5001), WebhookHandler)
print("Webhook receiver listening on port 5001", flush=True)
server.serve_forever()
