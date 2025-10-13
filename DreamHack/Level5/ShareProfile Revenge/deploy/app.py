from flask import Flask, request, render_template, g
from datetime import datetime, timedelta, timezone
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
import sqlite3
import jwt
import time
import threading

app = Flask(__name__)
app.secret_key = os.urandom(32)

DATABASE = "database.db"
FLAG = os.getenv("FLAG", "DH{FAKE_FLAG}")

def create_token(username):
    payload = {"username": username, "exp": datetime.now(timezone.utc) + timedelta(hours=1)}
    token = jwt.encode(payload, app.secret_key, algorithm="HS256")
    return token

def verify_token(token):
    try:
        decoded = jwt.decode(token, app.secret_key, algorithms=["HS256"])
        return decoded
    except:
        return None

def init_db():
    db = sqlite3.connect(DATABASE)
    db.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );
    """)
    db.execute("""
    CREATE TABLE IF NOT EXISTS profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        description TEXT DEFAULT '',
        image TEXT DEFAULT ''
    );
    """)
    db.execute(f"INSERT INTO users(username, password) VALUES ('admin', '{os.urandom(16).hex()}')")
    db.execute(f"INSERT INTO profiles(username, description, image) VALUES ('admin', 'Welcome! Share your profile with others.', '/static/admin.png')")
    db.commit()
    db.close()

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    db = get_db()
    profiles = db.execute("SELECT username, description, image FROM profiles ORDER BY id DESC").fetchall()

    token = request.args.get("token")
    if token and verify_token(token):
        return render_template("index.html", profiles=profiles, is_logged_in=True)
    return render_template("index.html", profiles=profiles, is_logged_in=False)

@app.route("/api/login", methods=["POST"])
def login():
    username = str(request.json.get("username"))
    password = str(request.json.get("password"))

    db = get_db()
    user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

    if user and user["password"] == password:
        token = create_token(user["username"])
        return {"status": "success", "token": token}
    return {"status": "error", "message": "Invalid credentials"}

@app.route("/api/register", methods=["POST"])
def register():
    username = str(request.json.get("username"))
    password = str(request.json.get("password"))

    try:
        db = get_db()
        db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        db.execute("INSERT OR IGNORE INTO profiles (username) VALUES (?)", (username,))
        db.commit()
        return {"status": "success"}
    except sqlite3.IntegrityError:
        return {"status": "error", "message": "User already exists"}
    except Exception:
        return {"status": "error", "message": "Registration failed"}

@app.route("/api/update_profile", methods=["POST"])
def update_profile():
    token = str(request.json.get("token"))

    decoded = verify_token(token)
    if not decoded:
        return {"status": "error", "message": "Invalid token"}

    username = decoded["username"]
    description = str(request.json.get("description", ""))
    image = str(request.json.get("image", ""))

    db = get_db()
    db.execute("UPDATE profiles SET description = ?, image = ? WHERE username = ?", (description, image, username))
    db.commit()

    return {"status": "success"}

@app.route("/api/admin", methods=["POST"])
def admin():
    token = str(request.json.get("token"))

    decoded = verify_token(token)
    if not decoded:
        return {"status": "error", "message": "Invalid token"}

    username = decoded["username"]
    if username != "admin":
        return {"status": "error", "message": "Access denied"}
    
    return {"status": "success", "flag": FLAG}

@app.route("/api/report", methods=["POST"])
def report():
    t = threading.Thread(target=check)
    t.start()

    return {"status": "success"}

def get_admin_password():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    admin = db.execute("SELECT * FROM users WHERE username = 'admin'").fetchone()
    db.close()
    return admin["password"]

def check():
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920x1080')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(5)

        driver.get("http://localhost:3000/")
        driver.find_element(By.ID, "username").send_keys("admin")
        driver.find_element(By.ID, "password").send_keys(get_admin_password())
        driver.find_element(By.ID, "loginBtn").click()
        time.sleep(1)

        driver.switch_to.alert.accept()
        time.sleep(1)

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    if not os.path.exists(DATABASE):
        init_db()
    app.run(host="0.0.0.0", port=3000)