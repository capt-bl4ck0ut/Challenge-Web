import unicodedata

def filter_code(user_input):
    banned_character = "'\"\\!@#$%^&*;:?_=<>~`"
    banned_word = [
        'eval', 'exec', 'import', 'open', 'os', 'sys',
        'read', 'system', 'write', 'sh', 'break', 'mro',
        'cat', 'flag', 'ascii', 'breakpoint', 'globals', 'init'
    ]
    test = unicodedata.normalize('NFKC', user_input)
    if user_input != test:
        return False
    for x in banned_word:
        if x in test:
            return False
    for x in banned_character:
        if x in test:
            return False

    return True


if __name__ == "__main__":
    n = input("Nhập chuỗi: ").strip()
    if filter_code(n):  
        print("[+] PASS")
    else:                
        print("[-] Fail")
