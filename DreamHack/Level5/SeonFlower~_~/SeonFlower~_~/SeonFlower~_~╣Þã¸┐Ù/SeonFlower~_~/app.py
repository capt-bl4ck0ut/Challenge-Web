from flask import Flask, request, render_template, redirect, session, abort
import requests
from urllib.parse import unquote
import os
import time
app = Flask(__name__)
app.secret_key = os.urandom(32)
login_attempts=0
path=''

def check_session():
    if not session:
        abort(403)
        
def check_Email(Email,PW):
    global login_attempts
    current_time = time.time()
    dif=current_time-login_attempts
    if(dif<5):
        return '3'
    login_attempts = current_time

    try:
        req=requests.get(f'http://localhost:9001/check?email={Email}&pw={PW}',timeout=10)
        return req.text
    except:
        return

def checkPath(path):
    try:
        req=requests.post('http://localhost:9001/checkPath',data={'path':path},timeout=10)
        req.raise_for_status()
        return req.text
    except:
        return 'gatcha'
def req(path):
    try:
        req=requests.get(f'http://localhost:9001/{path}',timeout=10)
        req.raise_for_status()
        return req.text
    except:
        return 'err'
    
def checkFlag(path):
    check=''.join(path)
    while('%' in check):
        check=unquote(check)
    if('flag' in check.lower()):
        return True
    else:
        return False

@app.route('/')
def index():
   return redirect('/login')

@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    Email=request.form['Email']
    PW=request.form['PW']
    ret=check_Email(Email,PW)
    if(ret=='1'):
        return '<script>alert(\'plz input valid email:(\')</script>'
    elif(ret=='2'):
        return '<script>alert(\'invalid pw!\')</script>'
    elif(ret=='3'):
        return '<script>alert(\'not yet...\')</script>'
    else:
        session['logged_in'] = True
        session['username'] = ret
        return redirect('/request')

@app.route('/request',methods=['GET', 'POST'])
def memo():
    check_session()
    global path
    path=request.form.getlist('path')
    if request.method == 'GET':
        return render_template('request.html',ID=session['username'])
    try:
        if(len(session['username'])>20):
            email=session['username'][:20]+'...'
        else:
            email=session['username']
            if(len(path)!=1):
                path='gatcha'
                path=checkPath(path)
                res=req(path)
                return render_template('request.html',ID=email,resp=res)
    except:
        email='whoru?'
    if(any('flag' in item.lower() for item in path) or checkFlag(path)):
        path='gatcha'

    path=checkPath(path)
    res=req(path)
    return render_template('request.html',ID=email,resp=res)

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect('/login')

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=9000, debug=False)