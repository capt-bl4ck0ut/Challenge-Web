#!/usr/bin/env python3
import base64
import glob
import os
import shutil
from urllib.parse import urlparse, parse_qs

import qrcode
from flask import Flask, abort, render_template, request, session

with open('./flag.txt', 'r') as f:
    FLAG = f.read()

app = Flask(__name__)
app.secret_key = os.urandom(32)

class CacheMiss(Exception):
    pass

def normalize_scheme(scheme):
    return scheme + '.'

def normalize_host(host):
    return host

def normalize_path(path):
    return path.replace('/', '.')

def normalize_params(params):
    return '.' + params

def normalize_query(query):
    q = parse_qs(query.replace('/', '.'))
    qs = ''
    for k, v in q.items():
        qs += k + '=' + v[-1] + '&'
    if len(qs) != 0:
        qs = qs[:-1]
    return qs

def normalize_fragment(fragment):
    return fragment

def normalize(url):
    p = urlparse(url)
    norm_url = normalize_scheme(p.scheme)
    norm_url += normalize_host(p.netloc)
    norm_url += normalize_path(p.path)
    norm_url += normalize_params(p.params)
    norm_url += normalize_query(p.query)
    norm_url += normalize_fragment(p.fragment)
    return norm_url

def get_cache(norm_url):
    cache = glob.glob('static/cache/' + norm_url)
    if len(cache) != 1:
        raise CacheMiss('Cache Miss!')
    return cache[0]

@app.before_request
def init_session():
    if session:
        return
    session['id'] = os.urandom(32).hex()
    os.mkdir('static/users/' + session['id'])

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/qr_generator', methods=['GET', 'POST'])
def qr_generator():
    if request.method == 'GET':
        return render_template('qr_generator.html')

    # POST
    url = request.form.get('url')
    if not isinstance(url, str):
        abort(400)

    try:
        norm_url = normalize(url)
        cache = get_cache(norm_url)
        # Cache Hit
        dst = 'static/users/' + session['id'] + '/qr_code.png'
        shutil.copyfile(cache, dst)

    except CacheMiss:
        img = qrcode.make(url)
        src = f'static/cache/{norm_url}'
        img.save(src)
        dst = 'static/users/' + session['id'] + '/qr_code.png'
        shutil.copyfile(src, dst)

    except:
        abort(500)

    finally:
        if url.startswith('http://') or url.startswith('https://'):
            with open(dst, 'rb') as f:
                img_data = base64.b64encode(f.read()).decode('utf-8')
            return f'<img src="data:image/png;base64,{img_data}">'
        return 'url must starts with "http://" or "https://".'

@app.route('/qr_reader', methods=['GET', 'POST'])
def qr_reader():
    if request.method == 'GET':
        return render_template('qr_reader.html')

    # POST
    return 'in maintenance.. 👷'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
