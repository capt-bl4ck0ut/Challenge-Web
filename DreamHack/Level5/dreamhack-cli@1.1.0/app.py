from flask import Flask, request
from os import urandom
import subprocess

app = Flask(__name__)
app.secret_key = urandom(32)

@app.route('/config', methods=['POST'])
def config():
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()
    try:
        subprocess.run(
            ['dh', 'config', f'--email={email}', f'--password={password}'], capture_output=True, text=True, timeout=50, shell=False
        )
        return 'Success!!!'
    except subprocess.TimeoutExpired:
        return 'Timeout !!!'

@app.route('/create', methods=['GET'])
def create():
    url = request.args.get('url', '').strip()
    if len(url) == 0:
        return 'Please enter dreamhack wargame url. Ex) ?url=https://dreamhack.io/wargame/challenges/927'
    print(url)
    try:
        response = subprocess.run(
            ['dh', 'create', f'{url}', '-d'], capture_output=True, text=True, timeout=50, shell=False
        )
        print(response.stdout)
        return 'Success!!! Reponse: ' + response.stdout
    except subprocess.TimeoutExpired:
        return 'Timeout !!!'
    
if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000)