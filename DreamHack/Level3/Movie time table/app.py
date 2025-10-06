from flask import Flask, render_template, request
import json
import sys
import io

app = Flask(__name__)

CONFIG = {
 "SECRET": "DH{fake-fake-fake}"
}

class DataConfig(object):
    def __init__(self, name):
        self.name = name

def print_data(format_string, config_data):
    return format_string.format(config_data=config_data)
     
config_data = DataConfig("How can I get the flag?")

@app.route('/',methods=['GET'])
def page1():    
    payload = request.args.get('body')
    sys.stdin = io.StringIO(payload)
    result = print_data(sys.stdin.readline(), config_data)
    return render_template('index.html', value=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)