from http.server import BaseHTTPRequestHandler, HTTPServer
from cryptography.hazmat.primitives.asymmetric import ed25519
import json
import time

HOST = "127.0.0.1"
PORT = 6969


def generate_signature(private_key_hex: str, sign_params: dict) -> str:
    """
    Sign message with Ed25519 using:
    message = str(timestamp) + method + urlPath + JSON.stringify(message, sorted keys, no spaces)

    sign_params = {
        'timestamp': str,
        'method': str,
        'urlPath': str,
        'message': dict
    }
    """
    for k in ("timestamp", "method", "urlPath", "message"):
        if k not in sign_params:
            raise ValueError(f"Missing sign_params field: {k}")

    message_str = json.dumps(sign_params["message"], sort_keys=True, separators=(",", ":"))

    # Construct the bytes to sign
    to_sign = (
        str(sign_params["timestamp"])
        + sign_params["method"]
        + sign_params["urlPath"]
        + message_str
    ).encode("utf-8")

    # Create an Ed25519 private key object from hex
    private_key_bytes = bytes.fromhex(private_key_hex)
    private_key_obj = ed25519.Ed25519PrivateKey.from_private_bytes(private_key_bytes)

    # Generate signature and return hex
    signature = private_key_obj.sign(to_sign)
    return signature.hex()


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def _send_json(self, code: int, payload: dict):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

    def do_POST(self):
        # Read request body
        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length) if content_length > 0 else b"{}"

        try:
            data = json.loads(raw_body)
        except json.JSONDecodeError:
            return self._send_json(400, {"error": "Invalid JSON format"})

        print("Incoming data:", data)

        required = ["Method", "URL", "SecretKey"]
        missing = [k for k in required if k not in data]
        if missing:
            return self._send_json(400, {"error": f"Missing required parameters: {', '.join(missing)}"})

        method = str(data["Method"]).upper()
        url_path = str(data["URL"])
        secret_key_hex = str(data["SecretKey"])

        ts = str(data.get("Timestamp") or int(time.time()))


        body_field = data.get("Body", "{}")
        if isinstance(body_field, dict) and "raw" in body_field:
            body_raw_str = body_field.get("raw") or ""
        elif isinstance(body_field, str):
            body_raw_str = body_field
        else:
            body_raw_str = ""


        try:
            body_json = json.loads(body_raw_str) if body_raw_str else {}
        except json.JSONDecodeError:
            body_json = {}


        sign_params = {
            "timestamp": ts,
            "method": method,
            "urlPath": url_path,
            "message": body_json,
        }

        try:
            signature_hex = generate_signature(secret_key_hex, sign_params)
        except Exception as e:
            print("Signature generation failed:", e)
            return self._send_json(400, {"error": f"Signature generation failed: {str(e)}"})

        response = {
            "Timestamp": ts,
            "Signature": signature_hex,
        }

        print("Response:", response)
        return self._send_json(200, response)

    def do_GET(self):
        return self._send_json(405, {"error": "Method Not Allowed. Use POST /generateSignature"})


def run(host: str = HOST, port: int = PORT):
    server_address = (host, port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Starting HTTP server on http://{host}:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run()



