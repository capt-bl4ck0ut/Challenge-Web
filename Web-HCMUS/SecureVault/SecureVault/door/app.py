import http.server
import urllib.request
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

FLAG_VAULT_URL = 'http://flag-vault:6969'
KEY_VAULT_URL = 'http://key-vault:1337'

class Handler(http.server.SimpleHTTPRequestHandler):
    def error(self):
        self.send_response(500)
        self.end_headers()
        self.wfile.write(b'Thieves are not allowed to access the vault')

    def open(self, url, path):
        try:
            request = urllib.request.Request(url)
            request.selector = path
            response = urllib.request.urlopen(request)
            return response.read()
        except:
            self.error()
            return None

    def do_GET(self):
        content = self.open(FLAG_VAULT_URL, self.path)
        if content is None:
            return None
        
        key_data = self.open(KEY_VAULT_URL, self.path)
        if key_data is None:
            return None

        try:
            pub_key = RSA.import_key(key_data)
            cipher = PKCS1_OAEP.new(pub_key)
            encrypted_content = cipher.encrypt(content)
        except Exception as e:
            self.error()
            return

        self.send_response(200)
        self.end_headers()
        self.wfile.write(encrypted_content)
        return
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        if not post_data:
            self.error()
            return
        
        try:
            key_data = self.open(KEY_VAULT_URL, 'default')
            if key_data is None:
                return None
            
            pub_key = RSA.import_key(key_data)
            cipher = PKCS1_OAEP.new(pub_key)
            encrypted_content = cipher.encrypt(post_data)
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(encrypted_content)
        except Exception as e:
            self.error()

http.server.HTTPServer(('0.0.0.0', 3000), Handler).serve_forever()
