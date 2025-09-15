from flask import Flask, request
import os
import subprocess

app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route("/", methods=["GET"])
def index():
    # Lấy từng key
    cmd = ['python3'] + list(request.args.keys())
    # python3 + "../../../usr/local/lib/python3.11/fileinput.py" + "/app/flag"
    cmd[1] += '.py'
    filter_codes = ['`', '$', '<', '>', '|', '&', '{', '}', '=', '*', '?', '!', ';', '"', ',', '\n']
    for filter_code in filter_codes:
        for arg in cmd:
            if filter_code in arg:
                return 'No hack _(:3)J'

    if os.path.exists(cmd[1]) == False:
        return 'No such file _(:3)J'
    # ?../../../usr/local/lib/python3.11/fileinput.py&/app/flag
    response = subprocess.run(
        cmd, capture_output=True, text=True
    )
    return response.stdout

app.run(host="0.0.0.0", port=9000)
