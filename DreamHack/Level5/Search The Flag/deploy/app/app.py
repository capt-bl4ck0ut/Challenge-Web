from flask import (
    Flask,
    request,
    render_template,
    session,
    redirect,
    abort,
    render_template_string,
)
from query import get_user, get_user_by_username, register_user, search_sentences
from not_found import not_found_template
from os import urandom
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from promise import Promise
from time import sleep


app = Flask(__name__)
app.secret_key = urandom(32)


@app.after_request
def csp(response):
    response.headers[
        "Content-Security-Policy"
    ] = "default-src 'self'; img-src *; style-src 'self' https://stackpath.bootstrapcdn.com/;"
    return response


@app.errorhandler(404)
def page_not_found(e):
    if not "keyword" in str(e.description):
        return render_template_string(not_found_template("page")), 404
    else:
        return render_template_string(not_found_template(e.description["keyword"])), 404


@app.route("/", methods=["GET"])
def index():
    if not session:
        return redirect("/login")
    else:
        return render_template("search.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

    if username == "" or password == "":
        return render_template("login.html", msg="Enter the username and password")

    try:
        user = get_user(username, password)

        if user:
            if user[1] == "admin":
                session["username"] = user[1]
                session["isAdmin"] = True
                return redirect("/search")
            else:
                session["username"] = user[1]
                session["isAdmin"] = False
                return redirect("/search")
        else:
            return render_template("login.html", msg="Login Failed..."), 401

    except Exception as e:
        abort(500)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "" or password == "":
            return render_template("signup.html", msg="Enter the username and password")

        try:
            user = get_user_by_username(username)
            if user == None:
                register_user(username, password)
                return redirect("/login")

            elif username == user[1]:
                return render_template("signup.html", msg="Duplicated username"), 403

        except Exception as e:
            abort(500)


@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("isAdmin", None)
    return redirect("/")


@app.route("/search", methods=["GET"])
def search():
    if not session:
        return redirect("/login")

    if request.method == "GET":
        keyword = request.args.get("keyword")

        if keyword == None:
            return render_template("search.html")

        if keyword == "":
            return render_template("search.html", msg="Enter the the keyword")

        if "}" in keyword:
            return render_template("search.html", msg="Not allowed string")

        sentence_list = []
        sentences = search_sentences(keyword)

        if sentences == None:
            abort(404, {"keyword": keyword})

        for sentence in sentences:
            if (session["isAdmin"] == False) and (sentence[2] == 1):
                continue
            else:
                sentence_list.append(sentence[1])

        if len(sentence_list) == 0:
            abort(404, {"keyword": keyword})

        return render_template("search.html", sentence_list=sentence_list)

    else:
        abort(500)


@app.route("/report", methods=["GET", "POST"])
def report():
    if not session:
        return redirect("/login")

    if request.method == "POST":
        path = request.form.get("path")
        if not path:
            return render_template("report.html", msg="fail")

        if path and path[0] == "/":
            path = path[1:]

        url = f"http://127.0.0.1:8000/{path}"
        if check_url(url):
            return render_template("report.html", msg="success")
        else:
            return render_template("report.html", msg="fail")

    elif request.method == "GET":
        return render_template("report.html")


def check_url(url):
    try:
        service = Service(executable_path="/chromedriver")
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

        driver_promise = Promise(driver.get("http://127.0.0.1:8000/login"))
        driver_promise.then(driver.find_element(By.NAME, "username").send_keys("admin"))
        driver_promise.then(
            driver.find_element(By.NAME, "password").send_keys("REDACTED!!!")
        )
        driver_promise = Promise(driver.find_element(By.ID, "submit").click())
        driver_promise.then(driver.get(url))
        driver_promise.then(sleep(0.5))

    except Exception as e:
        driver.quit()
        return False
    finally:
        driver.quit()
    return True


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
