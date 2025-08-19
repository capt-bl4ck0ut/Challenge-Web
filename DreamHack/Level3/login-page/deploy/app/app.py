#!/usr/bin/env python3
from threading import RLock
import base64
import os

from flask import Flask, redirect, render_template, request, session
import pymysql

with open('./flag', 'r') as f:
    FLAG = f.read()

MAX_LOGIN_TRIES = 6

SQL_BAN_LIST = [
    'update', 'extract', 'lpad', 'rpad', 'insert', 'values', '~', ':', '+',
    'union', 'end', 'schema', 'table', 'drop', 'delete', 'sleep', 'substring',
    'database', 'declare', 'count', 'exists', 'collate', 'like', '!', '"',
    '$', '%', '&', '+', '.', ':', '<', '>', 'delay', 'wait', 'order', 'alter'
]

app = Flask(__name__)
app.secret_key = os.urandom(32)

def connect_mysql():
    db = pymysql.connect(host='localhost',
                         port=3306,
                         user=os.environ['MYSQL_USER'],
                         passwd=os.environ['MYSQL_PASSWORD'],
                         db='reset_db',
                         charset='utf8')
    cursor = db.cursor()
    return db, cursor

def check_query_ban_list(query):
    for banned in SQL_BAN_LIST:
        if banned in query.lower():
            return False
    return True

def reset_password():
    global cursor, db

    # Generate new password.
    while True:
        new_password = base64.b64encode(base64.b64encode(os.urandom(16))).decode()
        if check_query_ban_list(new_password):
            break

    # Update new password.
    done = False
    while not done:
        try:
            query = 'UPDATE users SET password = %s WHERE username = \'admin\''
            cursor.execute(query, (new_password, ))
            db.commit()
            done = True
        except pymysql.err.InterfaceError:
            db.close()
            db, cursor = connect_mysql()

@app.route('/', methods=['GET', 'POST'])
def index():
    if session:
        return redirect('/login')

    if request.method == 'GET':
        return render_template('index.html')

    # POST
    # Set a session per user.
    if not session:
        session['id'] = os.urandom(16)
        session['tries'] = 0
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    global cursor, db

    if not session:
        return redirect('/')

    if request.method == 'GET':
        return render_template('login.html', msg=None)

    # POST
    # Try to login.
    args = request.form

    if 'username' not in args and 'password' not in args:
        return render_template('login.html', msg='Enter username and password.')

    elif 'username' not in args and 'password' in args:
        return render_template('login.html', msg='Enter username.')

    elif 'username' in args and 'password' not in args:
        return render_template('login.html', msg='Enter password.')

    username = args['username']
    password = args['password']

    if not username and not password:
        return render_template('login.html', msg='Enter username and password.')

    elif not username and password:
        return render_template('login.html', msg='Enter username.')

    elif username and not password:
        return render_template('login.html', msg='Enter password.')

    if not check_query_ban_list(username) \
            or not check_query_ban_list(password):
        reset_password()
        session['tries'] = 0
        msg = 'What? you are hacker! I reset password!'
        return render_template('login.html', msg=msg)

    # Query the user.
    done = False
    while not done:
        try:
            query = 'SELECT * FROM users WHERE username = \'{0}\' ' \
                    'AND password = \'{1}\''
            with lock:
                query = query.format(username, password)
                cursor.execute(query)
                ret = cursor.fetchone()
            done = True
        except pymysql.err.InterfaceError:
            db.close()
            db, cursor = connect_mysql()

    # Failed to login.
    if not ret:
        session['tries'] += 1
        tries = session['tries']
        remain_tries = MAX_LOGIN_TRIES - tries
        if remain_tries <= 0:
            reset_password()
            session['tries'] = 0
            msg = 'Password is reset.'
            msg = msg.format(remain_tries)
            return render_template('login.html', msg=msg)

        msg = 'Password will be reset after {0} unsuccessful login attempts.'
        msg = msg.format(remain_tries)
        return render_template('login.html', msg=msg)

    # Succeed to login but double-check.
    actual_username = ret[1]
    actual_password = ret[2]

    if username != actual_username or password != actual_password:
        reset_password()
        session['tries'] = 0
        msg = 'What? you are hacker! I reset password!'
        return render_template('login.html', msg=msg)

    # Print flag.
    return render_template('login.html', msg=FLAG)

if __name__ == '__main__':
    lock = RLock()
    db, cursor = connect_mysql()
    reset_password()
    app.run(host='0.0.0.0', port=8000)
    db.close()
