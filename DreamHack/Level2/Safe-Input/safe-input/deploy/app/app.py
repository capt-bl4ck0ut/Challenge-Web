from flask import Flask, redirect, request, render_template
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep
from os import urandom, environ
from urllib.parse import quote

app = Flask(__name__)
app.secretkey = urandom(32)

FLAG = environ.get("FLAG", "DH{fake_flag}")
PASSWORD = environ.get("PASSWORD", "1234")


def access_page(text, cookie={"name": "name", "value": "value"}):
    try:
        service = Service(executable_path="/chromedriver-linux64/chromedriver")
        options = webdriver.ChromeOptions()
        for _ in [
            "headless",
            "window-size=1920x1080",
            "disable-gpu",
            "no-sandbox",
            "disable-dev-shm-usage",
        ]:
            options.add_argument(_)
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(3)
        driver.set_page_load_timeout(3)
        driver.get(f"http://127.0.0.1:8000/")
        driver.add_cookie(cookie)
        driver.get(f"http://127.0.0.1:8000/test?text={quote(text)}")
        sleep(1)
    except Exception as e:
        print(e, flush=True)
        driver.quit()
        return False
    driver.quit()
    return True

@app.route("/", methods=["GET"])
def index():
    return redirect("/test")

@app.route("/test", methods=["GET"])
def intro():
    text = request.args.get("text")
    return render_template("test.html", test=text)


@app.route("/report", methods=["GET", "POST"])
def report():
    if request.method == "POST":
        text = request.form.get("text")
        if not text:
            return render_template("report.html", msg="fail")

        else:
            if access_page(text, cookie={"name": "flag", "value": FLAG}):
                return render_template("report.html", message="Success")
            else:
                return render_template("report.html", message="fail")
    else:
        return render_template("report.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
