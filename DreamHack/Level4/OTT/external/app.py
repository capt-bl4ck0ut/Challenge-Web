import os
import uuid
from datetime import datetime
from io import BytesIO
from urllib.parse import urlparse

import docx
import requests
from flask import (
    Flask,
    abort,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

AUTH_SERVICE_URL = "http://internal:3000"
FLAG = os.environ.get("FLAG", "acsc{FAKE_FLAG}")


session = requests.Session()
adapter = requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=10)
session.mount("http://", adapter)
session.mount("https://", adapter)


def username_rule(username: str) -> bool:
    return len(username) >= 3 and username.isalnum() and "admin" not in username.lower()


def get_user(token: str) -> dict:
    resp = session.get(
        f"{AUTH_SERVICE_URL}/user", params={"token": token}, timeout=(2, 5)
    )
    if resp.status_code != 200:
        abort(401)
    return resp.json()


@app.errorhandler(400)
def bad_request(error):
    return (
        render_template(
            "error.html",
            error_code="400",
            error_title="BAD REQUEST",
            error_message="Invalid request format or missing parameters.",
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            session_id=str(uuid.uuid4())[:8].upper(),
        ),
        400,
    )


@app.errorhandler(403)
def forbidden(error):
    return (
        render_template(
            "error.html",
            error_code="403",
            error_title="FORBIDDEN",
            error_message="Insufficient privileges. Admin access required.",
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            session_id=str(uuid.uuid4())[:8].upper(),
        ),
        403,
    )


@app.errorhandler(404)
def not_found(error):
    return (
        render_template(
            "error.html",
            error_code="404",
            error_title="NOT FOUND",
            error_message="The requested resource could not be located.",
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            session_id=str(uuid.uuid4())[:8].upper(),
        ),
        404,
    )


@app.errorhandler(500)
def internal_error(error):
    return (
        render_template(
            "error.html",
            error_code="500",
            error_title="INTERNAL ERROR",
            error_message="System malfunction detected. Please contact administrator.",
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            session_id=str(uuid.uuid4())[:8].upper(),
        ),
        500,
    )


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("user", "")
        if not username_rule(user):
            abort(400)

        resp = session.get(
            f"{AUTH_SERVICE_URL}/issue", params={"user": user}, timeout=(2, 5)
        )
        if resp.status_code != 200:
            abort(400)

        data = resp.json()
        token_xml = data.get("tokenXml")
        map_resp = session.get(
            f"{AUTH_SERVICE_URL}/map", params={"tokenXml": token_xml}, timeout=(2, 5)
        )
        if map_resp.status_code != 200:
            abort(401)

        token = map_resp.json().get("token")
        res = make_response(redirect(url_for("upload")))
        res.set_cookie("token", token)
        return res

    return render_template("login.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    token = request.cookies.get("token")
    user = get_user(token)
    if not user.get("valid"):
        abort(400)

    if request.method == "POST":
        if "file" not in request.files:
            abort(400)
        file = request.files["file"]
        if not file.filename.lower().endswith(".docx"):
            abort(400)

        try:
            text_content = []
            file_stream = BytesIO(file.read())
            doc = docx.Document(file_stream)

            for rel in doc.part.rels.values():
                if rel.is_external:
                    url = rel.reltype
                    if url.startswith(("http://", "https://")):
                        ext_resp = session.get(url, timeout=(2, 5))
                        if ext_resp.status_code == 200:
                            text_content.append(ext_resp.text)
                        else:
                            abort(400)

            text_content.extend(para.text for para in doc.paragraphs if para.text)

            return render_template("upload.html", content="\n".join(text_content))
        except Exception:
            abort(500)

    return render_template("upload.html")


@app.route("/flag")
def flag():
    token = request.cookies.get("token")
    if not token:
        abort(401)

    user = get_user(token)
    if not user.get("valid") or user.get("username") != "admin":
        abort(403)

    return {"flag": FLAG}


if __name__ == "__main__":
    app.jinja_env.cache = {}
    app.run(host="0.0.0.0", port=8000)
