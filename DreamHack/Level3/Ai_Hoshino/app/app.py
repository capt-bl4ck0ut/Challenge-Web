from flask import Flask, render_template, request, jsonify, redirect, url_for, render_template_string
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import string
from random import choice


def random_string(length):
    return ''.join(choice(string.ascii_letters + string.digits) for _ in range(length))

secret_token = random_string(30)
report_count = 0


with open('flag.txt', 'r') as file:
    FLAG = file.read().strip()


app = Flask(__name__)

@app.after_request
def set_header(response):
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Document-Policy'] = 'force-load-at-top'
    response.headers['Content-Security-Policy'] = "script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';"
    response.headers['Referrer-Policy'] = 'no-referrer'
    return response


@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')


@app.route('/admin', methods=["GET"])
def admin():
    if request.remote_addr == '127.0.0.1' and request.host == 'localhost':
        return render_template('admin.html',secret_token=secret_token), 200
    else:
        return render_template_string("""
        <script>
            alert("admin is not valid");
            window.history.back();
        </script>
        """), 404

@app.route('/secret', methods=["GET"])
def secret():
    if request.args.get("secret_token") != secret_token:
        return render_template_string("""
        <script>
            alert("secret token is not valid");
            window.history.back();
        </script>
        """), 404
    return FLAG


@app.route("/report", methods=["GET", "POST"])
def report():
    if request.method == "POST":
        global report_count
        report_count += 1
        if report_count >= 35:
            global secret_token
            secret_token = random_string(30)
            report_count = 0
        path = request.form.get("path")
        if not path:
            return render_template("report.html", msg="fail", report_count=report_count)
        if path.startswith("/"):
            path = path[1:]
        url = f"http://localhost/{path}"
        if check_url(url):
            return render_template("report.html", msg="success", report_count=report_count)
        else:
            return render_template("report.html", msg="fail", report_count=report_count)
    else:
        return render_template("report.html",report_count=report_count)


def check_url(url):
    try:
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--js-flags=--noexpose_wasm,--jitless')
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(3)
        driver.set_page_load_timeout(5)
        driver.get(url)
        driver.quit()
        return True
    except Exception as e:
        return False

if __name__ == '__main__':
    app.run(debug=False, port=80,host='0.0.0.0')
