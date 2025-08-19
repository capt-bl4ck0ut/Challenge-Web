#!/usr/bin/env python3
import json
import pprint
import subprocess
from flask import Flask, redirect, request, abort, render_template, url_for, g

POST = 'POST'
GET = 'GET'
PATCH = 'PATCH'
DELETE = 'DELETE'

BACKEND_BASE_URL = 'http://backend:8000'


app = Flask(__name__)


def curl_backend_api(path, method, client_host, token=None, data=None):
    try:
        args = [
            '/usr/bin/curl', f'{BACKEND_BASE_URL}{path}',
            '-H', f'Simple-Token: {token}',
            '-H', f'X-Forwarded-For: {client_host}',
            '-H', 'Content-Type: application/json',
            '-X', method,
            '--ignore-content-length',
            '--max-time', '0.3',
            '-d', json.dumps(data) if data else ''
        ]
        res = subprocess.run(args, capture_output=True)
        return res.stdout.decode()
    except:
        return None

def beautify(res):
    r = pprint.pformat(json.loads(res))
    return r


@app.before_request
def before_request():
    if request.path != '/' and not request.path.startswith('/static/'):
        g.simple_token = request.args.get('simple_token')
        if g.simple_token is None:
            abort(401)

@app.route('/', methods=['GET'])
def get_index():
    res = curl_backend_api('/auth', POST, request.remote_addr)

    simple_token = json.loads(res)

    return redirect(url_for('get_menu', simple_token=simple_token))

@app.route('/menu', methods=['GET'])
def get_menu():
    return render_template('menu.html', simple_token=g.simple_token)

@app.route('/create', methods=['GET'])
def get_create():
    return render_template('create.html', simple_token=g.simple_token)

@app.route('/create', methods=['POST'])
def post_create():
    title = request.form.get('title')
    content = request.form.get('content')
    author = request.form.get('author')

    if not isinstance(title, str) \
            or not isinstance(content, str) \
            or not isinstance(author, str):
        abort(400)

    data = {'title': title, 'content': content, 'author': author}
    res = curl_backend_api('/posts', POST, request.remote_addr, g.simple_token, data)
    if res is None:
        abort(400)

    return render_template('/api_result.html', simple_token=g.simple_token, res=beautify(res))

@app.route('/read', methods=['GET'])
def get_read():
    res = curl_backend_api('/posts', GET, request.remote_addr, g.simple_token)
    if res is None:
        abort(400)

    return render_template('/api_result.html', simple_token=g.simple_token, res=beautify(res))

@app.route('/update', methods=['GET'])
def get_update():
    return render_template('update.html', simple_token=g.simple_token)

@app.route('/update', methods=['POST'])
def post_update():
    post_idx = request.form.get('post_idx')
    title = request.form.get('title')
    content = request.form.get('content')
    author = request.form.get('author')

    if not isinstance(post_idx, str) \
            or not post_idx.isdecimal() \
            or not isinstance(title, str | None) \
            or not isinstance(content, str | None) \
            or not isinstance(author, str | None):
        abort(400)

    data = {'title': title, 'content': content, 'author': author}
    res = curl_backend_api(f'/posts/{post_idx}', PATCH, request.remote_addr, g.simple_token, data)
    if res is None:
        abort(400)

    return render_template('/api_result.html', simple_token=g.simple_token, res=beautify(res))

@app.route('/delete', methods=['GET'])
def get_delete():
    return render_template('delete.html', simple_token=g.simple_token)

@app.route('/delete', methods=['POST'])
def post_delete():
    post_idx = request.form.get('post_idx')
    if not isinstance(post_idx, str) or not post_idx.isdecimal():
        abort(400)

    res = curl_backend_api(f'/posts/{post_idx}', DELETE, request.remote_addr, g.simple_token)
    if res is None:
        abort(400)

    return render_template('/api_result.html', simple_token=g.simple_token, res=res)
