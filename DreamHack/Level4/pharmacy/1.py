import string

ct = "Toiywqvghh{z3c3l_Ogg_iu0j3_h0yb1pb_Dme1vmct5_zi_z3eo!}"
pt_prefix = "Securinets{"

# Suy khóa từ known-plaintext (Vigenère chuẩn: C = P + K mod 26)
key_idx = []
for c, p in zip(ct, pt_prefix):
    if c.isalpha() and p.isalpha():
        key_idx.append((ord(c.lower())-ord('a')
                        - (ord(p.lower())-ord('a'))) % 26)

def vigenere_decrypt_letters_only(s, key):
    res, j = [], 0
    for ch in s:
        if ch.isalpha():
            k = key[j % len(key)]
            base = ord('A') if ch.isupper() else ord('a')
            res.append(chr(( (ord(ch)-base - k) % 26 ) + base))
            j += 1
        else:
            res.append(ch)
    return ''.join(res)

print('Key:', ''.join(chr(k+ord('a')) for k in key_idx))  # bkgefiicop
print(vigenere_decrypt_letters_only(ct, key_idx))
