import urllib.parse
from flask import Flask, render_template, Response, request, abort, make_response
from werkzeug.exceptions import HTTPException
from time import sleep
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException, WebDriverException
import urllib
import jwt
import os

# This is my favourite cookie UwU
# - Firebird Chan
FLAG = os.getenv("FLAG")
JWT_SECRET = os.urandom(32)
blacklist = ["127.0.0.1", "localhost", "0.0.0.0"]

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[],
    storage_uri='memory://',
)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/flag', methods=['GET'])
def flag():
    try:
        if request.remote_addr == "127.0.0.1":
            if 'jwt' in request.cookies:
                data = jwt.decode(request.cookies.get('jwt'), JWT_SECRET, algorithms=["HS256"])
                if any(host in data['given_url'] for host in blacklist):
                    resp = make_response(render_template('flag.html', message="Flag"))
                    resp.set_cookie('cookie', FLAG)
                    return resp

        resp = make_response(render_template('flag.html', message="Flag"))
        resp.set_cookie('cookie', 'No Flag')
        return resp
    except:
        abort(500)

@app.route('/visit', methods=['GET'])
def firebird_chan():
    return render_template("visit.html", message="Share your favourite links with Firebird Chan!")

@app.route('/visit', methods=['POST'])
@limiter.limit('1 per 30 seconds')
def visit():
    collected_cookies = []
    try:
        url = request.form.get('url')
        url_parsed = urllib.parse.urlparse(url)
        if any(host in url_parsed.netloc for host in blacklist):
            return render_template('visit.html', message="Don't visit my flag page >_<")
        else:
            try:
                # Just to prevent redirects :)
                encoded_jwt = jwt.encode({"given_url": url}, JWT_SECRET, algorithm="HS256")
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument("--disable-gpu")
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--no-sandbox")
                driver = webdriver.Chrome(options=chrome_options)
                driver.implicitly_wait(3)
                driver.get("http://127.0.0.1")
                driver.add_cookie({"name": "jwt", "value": encoded_jwt})
                driver.get(url)
                driver.set_page_load_timeout(3)	
                collected_cookies.append(driver.get_cookies())
                driver.quit()
            except InvalidArgumentException:
                return render_template('visit.html', message="Please enter a URL!")
            except WebDriverException as e:
                return render_template('visit.html', message=f"Something went wrong!")
            else:
                return render_template('visit.html', message="Firebird Chan has visited your URL and brought back cookies!", cookie=collected_cookies)
    except:
        abort(500)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="80")