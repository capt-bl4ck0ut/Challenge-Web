from flask import Flask, request, render_template, render_template_string, Response, redirect, url_for
import lxml.etree as ET
import requests
import os

app = Flask(__name__)
FLAG = open('flag.txt').read().strip()
app.config['FLAG'] = FLAG
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html')

#@app.route('/upload', methods=['POST'])
    # The upload function is not provided for safety!


@app.route('/internal', methods=['POST'])
def internal():
    if request.remote_addr != '127.0.0.1':
        return '', 404
    data = request.form.get('data', '')
    return render_template_string(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)