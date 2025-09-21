#!/usr/bin/env python3
import socket
import sys
import time
import re

HOST = "4.211.254.205"
PORT = 1059

ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def recv_all_ready(sock, timeout=1.0, max_wait=4.0):
    """Read whatever is available for a short while; return decoded text."""
    sock.setblocking(False)
    start = time.time()
    buf = b""
    last = 0.0
    while time.time() - start < max_wait:
        try:
            chunk = sock.recv(4096)
            if chunk:
                buf += chunk
                last = time.time()
            else:
                time.sleep(0.05)
        except BlockingIOError:
            # nothing ready; wait a hair
            time.sleep(0.05)
            if time.time() - last > timeout:
                break
    sock.setblocking(True)
    try:
        return buf.decode(errors="ignore")
    except:
        return buf.decode("latin-1", errors="ignore")

def sendline(sock, s):
    if not s.endswith("\n"):
        s = s + "\n"
    sock.sendall(s.encode())

def extract_cipher_candidates(text):
    """Return a list of candidate ciphertext-like tokens from a blob of text.
    We consider tokens that have many A-Z characters (e.g., >= 12) or are inside quotes after 'Ciphertext:'
    """
    cands = []
    # Direct patterns
    m = re.findall(r"Ciphertext[:\s]+([A-Za-z0-9{}_\-\!\?\.\,\:\;\(\)\[\] ]+)", text)
    for t in m:
        cands.append(t.strip())

    # Fallback: take long all-caps-ish sequences
    for line in text.splitlines():
        # strip ANSI
        line = re.sub(r"\x1b\[[0-9;]*m", "", line)
        if len(re.findall(r"[A-Za-z]", line)) >= 12:
            cands.append(line.strip())

    # de-dup while preserving order
    seen = set()
    out = []
    for t in cands:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out

def letters_only(s):
    return re.sub(r"[^A-Za-z]", "", s)

def to_upper_letters(s):
    return re.sub(r"[^A-Z]", "", s.upper())

def minimal_period(s):
    """Return minimal period of string s (assumes s is non-empty)."""
    # prefix-function (KMP) method
    n = len(s)
    if n == 0:
        return 0
    pi = [0]*n
    for i in range(1, n):
        j = pi[i-1]
        while j > 0 and s[i] != s[j]:
            j = pi[j-1]
        if s[i] == s[j]:
            j += 1
        pi[i] = j
    p = n - pi[-1]
    if p != 0 and n % p == 0:
        return p
    return n

def build_positional_mapping_from_query3(cipher_letters, m):
    """Given the ciphertext letters from the special Query3 of length 26*m,
    reconstruct per-position mapping tables E_i: P->C and inverse tables D_i: C->P.
    """
    if len(cipher_letters) < 26*m:
        raise ValueError(f"Need at least {26*m} letters from query3, got {len(cipher_letters)}")
    cipher_letters = cipher_letters[:26*m]

    E = [dict() for _ in range(m)]  # forward: plaintext->cipher
    D = [dict() for _ in range(m)]  # inverse: cipher->plaintext

    for i in range(m):
        # For fixed position i, the letters come from indices n = k*m + i for k=0..25,
        # and the plaintext there was ALPHA[k].
        for k in range(26):
            n = k*m + i
            c = cipher_letters[n]
            p = ALPHA[k]
            E[i][p] = c
            D[i][c] = p
    return E, D

def decrypt_with_tables(ciphertext, D):
    """Decrypt ciphertext using inverse tables D for letters A-Z; preserve case and non-letters."""
    m = len(D)
    out = []
    pos = 0  # counts only letters
    for ch in ciphertext:
        if ch.isalpha():
            i = pos % m
            up = ch.upper()
            if up in D[i]:
                plain_up = D[i][up]
            else:
                # If unseen mapping (unlikely), leave as-is
                plain_up = up
            # restore case
            if ch.islower():
                out.append(plain_up.lower())
            else:
                out.append(plain_up)
            pos += 1
        else:
            out.append(ch)
    return "".join(out)

def cipher_diff_is_constant(cA, cB):
    """Check whether (B - A) mod 26 is constant across positions (Vigenère variants)."""
    L = min(len(cA), len(cB))
    if L == 0:
        return False, None
    diffs = []
    for i in range(L):
        a = ord(cA[i]) - ord('A')
        b = ord(cB[i]) - ord('A')
        diffs.append((b - a) % 26)
    ok = all(d == diffs[0] for d in diffs)
    return ok, (diffs[0] if ok else None)

def build_key_shifts_from_A(A_letters):
    """Assuming classic variants:
       - Vigenère or Beaufort: shift = A_letters[i]-'A'
       - Variant Beaufort: shift = (26 - (A_letters[i]-'A')) % 26
       We'll detect which using a 'B' query.
    """
    return [(ord(c) - ord('A')) % 26 for c in A_letters]

def decrypt_shift_cycle(ciphertext, shifts, mode):
    """Decrypt assuming periodic shifts 'shifts' and 'mode' in {'vigenere','beaufort','variant_beaufort'}.
       Applies to letters only; preserves case.
    """
    out = []
    pos = 0
    m = len(shifts)
    for ch in ciphertext:
        if ch.isalpha():
            s = shifts[pos % m]
            up = ch.upper()
            x = ord(up) - ord('A')
            if mode == 'vigenere':
                p = (x - s) % 26
            elif mode == 'beaufort':
                # C = K - P -> P = K - C
                p = (s - x) % 26
            elif mode == 'variant_beaufort':
                # C = P - K -> P = C + K
                p = (x + s) % 26
            else:
                p = x
            chp = chr(p + ord('A'))
            out.append(chp if ch.isupper() else chp.lower())
            pos += 1
        else:
            out.append(ch)
    return "".join(out)

def main():
    print(f"[+] Connecting to {HOST}:{PORT} ...")
    sock = socket.create_connection((HOST, PORT), timeout=8.0)
    banner = recv_all_ready(sock, timeout=0.5, max_wait=2.0)
    if banner:
        print("[server]\n" + banner)

    # === Query 1: 'A' * N to learn period and maybe key-like sequence
    N = 2048
    q1 = "A" * N
    print(f"[>] Q1 (len={len(q1)}): first 64 chars shown:\n{q1[:64]}...")
    sendline(sock, q1)
    time.sleep(0.2)
    resp1 = recv_all_ready(sock, timeout=0.4, max_wait=2.0)
    print("[server]\n" + resp1)
    cands1 = extract_cipher_candidates(resp1)
    if not cands1:
        print("[-] Could not find ciphertext in response to Q1.")
        sys.exit(1)
    ct1 = cands1[-1]  # try last seen
    ct1_letters = to_upper_letters(ct1)
    if len(ct1_letters) < 64:
        print("[-] Ciphertext 1 too short / not letters. Aborting.")
        sys.exit(1)

    m = minimal_period(ct1_letters)
    print(f"[+] Estimated period m = {m}")

    # === Query 2: 'B' * N to disambiguate mode (optional but useful fallback)
    q2 = "B" * N
    print(f"[>] Q2 (len={len(q2)}): first 64 chars shown:\n{q2[:64]}...")
    sendline(sock, q2)
    time.sleep(0.2)
    resp2 = recv_all_ready(sock, timeout=0.4, max_wait=2.0)
    print("[server)\n" + resp2)
    cands2 = extract_cipher_candidates(resp2)
    if not cands2:
        print("[-] Could not find ciphertext in response to Q2.")
        sys.exit(1)
    ct2 = cands2[-1]
    ct2_letters = to_upper_letters(ct2)

    ok_diff, diff = cipher_diff_is_constant(ct1_letters[:len(ct2_letters)], ct2_letters)
    print(f"[+] Constant (B-A) mod 26 across positions? {ok_diff} (diff={diff})")

    # === Query 3: Build full per-position mapping in one go (length = 26*m)
    L3 = 26 * m
    q3 = "".join(ALPHA[n // m] for n in range(L3))
    print(f"[>] Q3 mapping probe (len={len(q3)}). This learns full A..Z mapping at each position.")
    sendline(sock, q3)
    time.sleep(0.2)
    resp3 = recv_all_ready(sock, timeout=0.6, max_wait=3.0)
    print("[server]\n" + resp3)
    cands3 = extract_cipher_candidates(resp3)
    if not cands3:
        print("[-] Could not find ciphertext in response to Q3 mapping probe.")
        sys.exit(1)
    ct3 = cands3[-1]
    ct3_letters = to_upper_letters(ct3)

    use_tables = True
    try:
        E, D = build_positional_mapping_from_query3(ct3_letters, m)
        print("[+] Built per-position mapping tables successfully.")
    except Exception as e:
        print(f"[!] Mapping build failed ({e}). Will try key-shift fallback (Vigenère/Beaufort family).")
        use_tables = False

    # After 3 queries, the server should now send the 'something' (target ciphertext)
    print("[*] Waiting for the final challenge ciphertext...")
    time.sleep(0.5)
    tail = recv_all_ready(sock, timeout=0.6, max_wait=4.0)
    print("[server]\n" + tail)
    candsF = extract_cipher_candidates(tail)
    if not candsF:
        print("[?] Could not automatically detect final ciphertext. Please paste it here:")
        final_ct = sys.stdin.readline().strip()
    else:
        final_ct = candsF[-1]
    print(f"[+] Final ciphertext candidate:\n{final_ct}\n")

    if use_tables:
        plaintext = decrypt_with_tables(final_ct, D)
    else:
        # fallback: try Vigenère / Beaufort / Variant Beaufort using shifts from Q1 'A's
        shifts = build_key_shifts_from_A(ct1_letters[:m])
        mode_order = []
        if ok_diff and diff == 1:
            mode_order = ['vigenere', 'variant_beaufort', 'beaufort']
        elif ok_diff and diff == 25:
            mode_order = ['beaufort', 'vigenere', 'variant_beaufort']
        else:
            mode_order = ['vigenere', 'variant_beaufort', 'beaufort']

        plaintext = None
        for mode in mode_order:
            candidate = decrypt_shift_cycle(final_ct, shifts, mode)
            if "Securinets{" in candidate or "SECURINETS{" in candidate or "Securinets" in candidate:
                plaintext = candidate
                print(f"[+] Mode likely: {mode}")
                break
        if plaintext is None:
            # just pick vigenere
            plaintext = decrypt_shift_cycle(final_ct, shifts, 'vigenere')

    print("[+] Decrypted message:\n" + plaintext)
    # try to extract the flag
    mflag = re.search(r"Securinets\{[^}]+\}", plaintext)
    if mflag:
        print("\n[FLAG] " + mflag.group(0))
    else:
        print("\n[!] FLAG pattern not found automatically. Check the plaintext above.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("[-] Error:", e)
        sys.exit(1)
