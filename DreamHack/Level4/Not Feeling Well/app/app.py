from flask import Flask, request, render_template, session, url_for, redirect, flash
from utils import info, waf, file_loader, db_integrity, manager, escape
import logging
import os
import re

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(
    __name__,
    static_folder='static/',
    template_folder='templates/'
)
app.secret_key = os.urandom(26)

print(os.environ.pop('FLAG'))

@app.route('/', methods = ['GET'])
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])

    return render_template('index.html')

@app.route('/mypage', methods = ['GET', 'POST'])
def mypage():
    if request.method == 'GET':
        if 'username' in session:

            image = file_loader(session['profile'])

            return render_template('mypage.html', username=session['username'], status_message=session['status_message'], image=image)

        flash("plz login")
        flash("/signin")
        return render_template("mypage.html")

    elif request.method == 'POST':

        if 'username' not in session:
            flash('plz login')
            flash('/signin')
            return render_template('mypage.html')

        edit = request.form.get('edit', '')

        if edit == 'username':
            username = request.form.get('username','')

            if waf(username, 'sqli') and len(username) > 15:
                flash('no hack!')
                return render_template('mypage.html')

            sess_username = session['username']
            sess_profile = session['profile']
            sess_status_message = session['status_message']

            conn = manager()
            conn.cursor()
            conn.execute(f"""
                UPDATE `users` SET `username` = '{username}' WHERE `status_message` = '{sess_status_message}' and `username` = '{sess_username}' and `profile` = '{sess_profile}'
            """)

            conn.commit()
            conn.close()
            
            user_info = {
                    'username':request.form.get('username', ''),
                    'profile':sess_profile,
                    'status_message':sess_status_message
            }

            if db_integrity(user_info):
                flash('no hack!')
                return render_template('mypage.html')

            session.clear()

            flash('success update!\\nnplz login again!')
            flash('/signin.html')
            return render_template('mypage.html')

        if edit == 'profile':
            profile = request.form.get('profile', 'simple.png')

            sess_username = session['username']
            sess_profile = session['profile']
            sess_status_message = session['status_message']

            if not re.search('^\/app\/static\/images\/([a-zA-Z0-9]+\.[a-zA-Z0-9]+)$', profile):
                flash('no hack!')
                return render_template('mypage.html')
    
            conn = manager()
            conn.cursor()
            conn.execute(f"""
                UPDATE `users` SET `profile` = '{profile}' WHERE `status_message` = '{sess_status_message}' and `username` = '{sess_username}' and `profile` = '{sess_profile}'
            """)

            conn.commit()
            conn.close()

            user_info = {
                    'username':sess_username,
                    'profile':request.form.get('profile', ''),
                    'status_message':sess_status_message
            }

            if db_integrity(user_info):
                flash('no hack!')
                return render_template('mypage.html')
                
            session.clear()

            flash('success update!\\nplz login again!')
            flash('/signin.html')
            return render_template('mypage.html')

        if edit == 'status_message':
            status_message = escape(request.form.get('status_message', 'Hello! Simple Message'))

            sess_username = session['username']
            sess_profile = session['profile']
            sess_status_message = session['status_message']

            if waf(status_message, 'sqli') and len(status_message) > 100:
                flash('no hack!')
                return render_template('mypage.html')

            conn = manager()
            conn.cursor()
            conn.execute(f"""
                UPDATE `users` SET `status_message` = '{status_message}' WHERE `status_message` = '{sess_status_message}' and `username` = '{sess_username}' and `profile` = '{sess_profile}'
            """)

            conn.commit()
            conn.close()

            user_info = {
                    'username':sess_username,
                    'profile':sess_profile,
                    'status_message':request.form.get('status_message', '')
            }

            if db_integrity(user_info):
                flash('no hack!')
                return render_template('mypage.html')


            session.clear()

            flash('success update!\\nplz login again!')
            flash('/signin.html')
            return render_template('mypage.html')

        else:
            flash('Wrong Edit!')
            return render_template('mypage.html')

@app.route('/signin', methods = ['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template('signin.html')

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        if len(username) > 15 or len(password) > 15:
            flash('no hack!')
            return render_template('signin.html')

        if waf(username, 'sqli') or waf(password, 'sqli'):
            flash('no hack!')
            return render_template('signin.html')

        conn = manager()
        conn.cursor()

        conn.execute(f"""
            SELECT `username`, `password`, `profile`, `status_message` FROM `users` WHERE `username` = '{username}'
        """)

        res = conn.fetch_all()[0]

        conn.close()

        if 'username' in res:
            
            if res['password'] != password:
                flash('Login Failed!')

            session['username'] = escape(res['username'])
            session['profile'] = escape(res['profile'])
            session['status_message'] = escape(res['status_message'])
            
            flash(f'Hello {username}!')
            flash('/')
            return render_template('signin.html')

        else:
            flash('Login Failed!')
            return render_template('signin.html')

app.run('0.0.0.0', 8080)
