import http.server
from Crypto.PublicKey import RSA

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        base_name = self.path.strip("/").replace("/", "_") or "default"
        pub_key_path = f"{base_name}"
        priv_key_path = f"private_{base_name}"

        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key()

        with open(priv_key_path, "wb") as f:
            f.write(private_key)

        with open(pub_key_path, "wb") as f:
            f.write(public_key)

        super().do_GET()

http.server.HTTPServer(('0.0.0.0', 1337), Handler).serve_forever()
