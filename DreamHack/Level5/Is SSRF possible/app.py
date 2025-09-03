from flask import Flask, request, jsonify
import re
import ipaddress
import socket
import time
import hashlib
import requests
app = Flask(__name__)

flag = "d23b51c4e4d5f7c4e842476fea4be33ba8de9607dfe727c5024c66f78052b70a"

def sha256_hash(text):
    text_bytes = text.encode('utf-8')
    sha256 = hashlib.sha256()
    sha256.update(text_bytes)
    hash_hex = sha256.hexdigest()
    return hash_hex

isSafe = False
def check_ssrf(url,checked):
    global isSafe
    if "@" in url or "#" in url:
        isSafe = False
        return "Fail"
    if checked > 3:
        print("Các URL chuyển hướng quá 3 lần đều bị cấm.")
        isSafe = False
        return "Fail"
    protocol = re.match(r'^[^:]+', url)
    if protocol is None:
        isSafe = False
        print("Không phát hiện thấy giao thức nào.")
        return "Fail"
    print("Protocol :",protocol.group())
    if protocol.group() == "http" or protocol.group() == "https":
        host = re.search(r'(?<=//)[^/]+', url)
        print(host.group())
        if host is None:
            isSafe = False
            print("Không phát hiện được máy chủ nào.")
            return "Fail"
        host = host.group()
        print("Host :",host)
        try:
            ip_address = socket.gethostbyname(host)
        except:
            print("Máy chủ không chính xác.")
            isSafe = False
            return "Fail"
        for _ in range(60): # DNS Rebinding 공격을 방지하기 위한 반복문, 1분간 검사
            print("Đang xác minh IP.", _)
            ip_address = socket.gethostbyname(host) # 호스트로부터 IP를 가져옵니다.
            if ipaddress.ip_address(ip_address).is_private: # 두 IP 중 하나의 IP라도 내부IP라면
                print("Đã phát hiện IP mạng nội bộ. ")
                isSafe = False
                return "Fail"
            time.sleep(1) # 1초 대기
        print("Xác nhận chuyển hướng : ",url)
        try:
            response = requests.get(url,allow_redirects=False) # 요청을 전송합니다. 검증을 마친 URL이기에 안전합니다.
            if 300 <= response.status_code and response.status_code <= 309:
                redirect_url = response.headers['location']  # 이동되는 URL을 가져옵니다.
                print("Đã phát hiện chuyển hướng.",redirect_url)
                if len(redirect_url) >= 120:
                    isSafe = False
                    return "fail"
                check_ssrf(redirect_url,checked + 1) # 리다이렉션 횟수를 카운팅함과 동시에 안전한 지 확인합니다.
        except:
            print("URL 요청에 실패했습니다.")
            isSafe = False
            return "Fail"
        if isSafe == True:
            print("URL 등록에 성공했습니다.")
            return "SUCCESS"
        else:
            return "Fail"

    else:
        print("Đảm bảo URL bắt đầu bằng HTTP/HTTPS.")
        isSafe = False
        return "Fail"

@app.route('/check-url', methods=['POST'])
def check_url():
    global isSafe
    data = request.get_json()
    if 'url' not in data:
        return jsonify({'error': 'No URL provided'}), 400

    url = data['url']
    host = re.search(r'(?<=//)[^/]+', url)
    print(host.group())
    if host is None:
        print("Không phát hiện được máy chủ nào")
        return "Fail"
    host = host.group()
    if host != "www.google.com":
        isSafe = False
        return "Máy chủ phải là www.google.com"
    isSafe = True
    result = check_ssrf(url,1)
    if result != "SUCCESS" or isSafe != True:
        return "Đây là URL có thể gây ra SSRF."
    try:
        response = requests.get(url)
        status_code = response.status_code
        return jsonify({'url': url, 'status_code': status_code})
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Request Failed.'}), 500
    
@app.route('/admin',methods=['GET'])
def admin():
    global flag
    user_ip = request.remote_addr
    if user_ip != "127.0.0.1":
        return "only localhost."
    if request.args.get('nickname'):
        nickname = request.args.get('nickname')
        flag = sha256_hash(nickname)
        return "success."

@app.route("/flag",methods=['POST'])
def clear():
    global flag
    if flag == sha256_hash(request.args.get('nickname')):
        return "DH{REDACTED}"
    else:
        return "you can't bypass SSRF-FILTER zzlol 😛"

if __name__ == '__main__':
    print("Hash : ",sha256_hash("Hãy cho chúng tôi thấy những ý tưởng tấn công sáng tạo của bạn!"))
    app.run(debug=False,host='0.0.0.0',port=80)
