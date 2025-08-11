from flask import Flask, render_template, request, jsonify
import random
import subprocess

app = Flask(__name__)
TOKEN = "{**SWAPED**}"
FLAG = "SWAP{sample_flag}"
BLACK_LIST = ['file', 'dict', 'sftp', 'tftp', 'ldap', 'netdoc', 'localhost', 'gopher', '127.0.0.1']
PASSWORD = f"{random.randint(0, 255):02X}"
ALLOW_HOST = ['abcd.com', 'asdf.com', 'example.com']
print("password is : " + PASSWORD)

@app.route('/')
def swap():
    return render_template('index.html')

@app.route('/user-page', methods=['GET'])
def user():
    url = request.args.get('url')

    if not url:
        return jsonify({"swap": "Write URL"}), 400

    if not any(allow in url for allow in ALLOW_HOST):
        return jsonify({"swap": "URL not allowed"}), 403

    for bad in BLACK_LIST:
        if bad in url.lower():
            return jsonify({"swap": "BAN LIST"}), 403

    try:
        result = subprocess.run(
            ["curl", "-s", url],
            text=True,
            capture_output=True,
            check=True
        )
        return jsonify({"response": result.stdout})

    except subprocess.CalledProcessError as e:
        return jsonify({"swap": "Error!~", "details": str(e)}), 500
@app.route('/access-token', methods=['GET'])
def admin():
    if request.remote_addr in ["127.0.0.1"]:
        password = request.args.get("password")

        if password:
            if password == PASSWORD:
                return jsonify({"server": TOKEN}), 200
            else:
                return jsonify({"server": "Nop~ Password Wrong><"}), 403
        else:
            return jsonify({"server": "Write Password!"}), 400
    else:
        return jsonify({"server": "Only Localhost Can Access : )"}), 403

@app.route('/admin', methods=['GET'])
def check():
    if request.args.get("token") == TOKEN:
        return "<h1>dotori-company : $#@&*(@#&*(@)) BeePPP.. </h1>" + FLAG
    else:
        return jsonify({"server": "you are not admin..."}), 403

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
    print("Ready Yeah~! made by swap ENJOY:)")
