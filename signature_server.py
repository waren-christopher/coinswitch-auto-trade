# from cryptography.hazmat.primitives.asymmetric import ed25519
# from http.server import BaseHTTPRequestHandler, HTTPServer
# import json
# import time


# def generate_signature(private_key, sign_params):
#     try:
#         # Convert the private key and message to bytes
#         private_key_bytes = bytes.fromhex(private_key)
#         message_str = json.dumps(sign_params["message"], sort_keys=True, separators=(',', ':'))
#         message_bytes = bytes(str(sign_params["timestamp"]) + sign_params["method"] + sign_params["urlPath"] + message_str, 'utf-8')

#         # Create an Ed25519 private key object
#         private_key_obj = ed25519.Ed25519PrivateKey.from_private_bytes(private_key_bytes)

#         # Generate the signature
#         signature = private_key_obj.sign(message_bytes)

#         return signature.hex()
#     except ValueError as e:
#         print("Signature generation failed:", e)
#         return None


# class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

#     def do_GET(self):
#         # Parse Content-Length to read the body
#         content_length = int(self.headers['Content-Length'])
#         post_data = self.rfile.read(content_length)

#         try:
#             # Parse JSON body
#             data = json.loads(post_data)

#             body = data.get("Body", "{}")
#             print(data, body)
#             missing = []
#             if 'Method' not in data :
#                 missing.append('Method')
#             if 'URL' not in data:
#                 missing.append('Method')
#             if 'SecretKey' not in data:
#                 missing.append('Method')

#             if missing:
#                 self.send_response(400)
#                 self.send_header("Content-Type", "application/json")
#                 self.end_headers()
#                 self.wfile.write(json.dumps({"error": f"Missing required parameters, {' '.join(missing)}"}).encode())
#                 return

#             # Generate timestamp
#             timestamp = str(int(time.time()))
#             body_parsed = json.loads(body.get('raw', '{}'))

#             sign_params = {
#                 "timestamp": timestamp,
#                 "method": data['Method'],
#                 "urlPath":  data['URL'],
#                 "message": body_parsed
#             }
#             # Prepare response
#             signature = generate_signature(data['SecretKey'], sign_params)

#             response = {
#                 "Timestamp": timestamp,
#                 "Signature": signature
#             }
#             print(response)

#             # Send success response
#             self.send_response(200)
#             self.send_header("Content-Type", "application/json")
#             self.end_headers()
#             self.wfile.write(json.dumps(response).encode())

#         except json.JSONDecodeError:
#             # Handle JSON parsing error
#             self.send_response(400)
#             self.send_header("Content-Type", "application/json")
#             self.end_headers()
#             self.wfile.write(json.dumps({"error": "Invalid JSON format"}).encode())


# def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
#     server_address = ('', port)
#     httpd = server_class(server_address, handler_class)
#     print(f"Starting HTTP server on port {port}")
#     httpd.serve_forever()


# if __name__ == "__main__":
#     run()


# from cryptography.hazmat.primitives.asymmetric import ed25519
# from http.server import BaseHTTPRequestHandler, HTTPServer
# import json
# import time


# def generate_signature(private_key, sign_params):
#     try:
#         # Convert the private key and message to bytes
#         private_key_bytes = bytes.fromhex(private_key)
#         message_str = json.dumps(sign_params["message"], sort_keys=True, separators=(',', ':'))
#         message_bytes = bytes(
#             str(sign_params["timestamp"]) + sign_params["method"] + sign_params["urlPath"] + message_str,
#             'utf-8'
#         )

#         # Create an Ed25519 private key object
#         private_key_obj = ed25519.Ed25519PrivateKey.from_private_bytes(private_key_bytes)

#         # Generate the signature
#         signature = private_key_obj.sign(message_bytes)

#         return signature.hex()
#     except ValueError as e:
#         print("Signature generation failed:", e)
#         return None


# class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

#     def do_GET(self):
#         # Parse Content-Length to read the body
#         content_length = int(self.headers.get('Content-Length', 0))
#         post_data = self.rfile.read(content_length) if content_length > 0 else b"{}"

#         try:
#             # Parse JSON body
#             data = json.loads(post_data)

#             body = data.get("Body", "{}")
#             print("Incoming data:", data)

#             missing = []
#             if 'Method' not in data:
#                 missing.append('Method')
#             if 'URL' not in data:
#                 missing.append('URL')
#             if 'SecretKey' not in data:
#                 missing.append('SecretKey')

#             if missing:
#                 self.send_response(400)
#                 self.send_header("Content-Type", "application/json")
#                 self.end_headers()
#                 self.wfile.write(json.dumps({"error": f"Missing required parameters: {', '.join(missing)}"}).encode())
#                 return

#             # Generate timestamp
#             timestamp = str(int(time.time()))
#             body_parsed = json.loads(body.get('raw', '{}')) if isinstance(body, dict) else json.loads(body)

#             sign_params = {
#                 "timestamp": timestamp,
#                 "method": data['Method'],
#                 "urlPath": data['URL'],
#                 "message": body_parsed
#             }

#             # Generate signature
#             signature = generate_signature(data['SecretKey'], sign_params)

#             response = {
#                 "Timestamp": timestamp,
#                 "Signature": signature
#             }
#             print("Response:", response)

#             # Send success response
#             self.send_response(200)
#             self.send_header("Content-Type", "application/json")
#             self.end_headers()
#             self.wfile.write(json.dumps(response).encode())

#         except json.JSONDecodeError:
#             # Handle JSON parsing error
#             self.send_response(400)
#             self.send_header("Content-Type", "application/json")
#             self.end_headers()
#             self.wfile.write(json.dumps({"error": "Invalid JSON format"}).encode())


# def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, host='127.0.0.1', port=6969):
#     server_address = (host, port)
#     httpd = server_class(server_address, handler_class)
#     print(f"Starting HTTP server on http://{host}:{port}")
#     httpd.serve_forever()


# if __name__ == "__main__":
#     run()



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
    # Validate inputs
    for k in ("timestamp", "method", "urlPath", "message"):
        if k not in sign_params:
            raise ValueError(f"Missing sign_params field: {k}")

    # Normalize message JSON to canonical string
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

        # Validate required fields
        required = ["Method", "URL", "SecretKey"]
        missing = [k for k in required if k not in data]
        if missing:
            return self._send_json(400, {"error": f"Missing required parameters: {', '.join(missing)}"})

        method = str(data["Method"]).upper()
        url_path = str(data["URL"])
        secret_key_hex = str(data["SecretKey"])

        # Timestamp: use provided Timestamp if present, otherwise current time
        ts = str(data.get("Timestamp") or int(time.time()))

        # Body can be raw string or object with { raw: string }
        body_field = data.get("Body", "{}")
        if isinstance(body_field, dict) and "raw" in body_field:
            body_raw_str = body_field.get("raw") or ""
        elif isinstance(body_field, str):
            body_raw_str = body_field
        else:
            body_raw_str = ""

        # Parse body JSON for canonical signing
        try:
            body_json = json.loads(body_raw_str) if body_raw_str else {}
        except json.JSONDecodeError:
            body_json = {}

        # Build signing parameters
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

    # Optional: handle GET clearly
    def do_GET(self):
        return self._send_json(405, {"error": "Method Not Allowed. Use POST /generateSignature"})


def run(host: str = HOST, port: int = PORT):
    server_address = (host, port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Starting HTTP server on http://{host}:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run()



