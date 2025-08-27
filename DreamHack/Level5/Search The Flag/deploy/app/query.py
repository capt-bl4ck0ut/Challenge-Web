from connections import connect_mysql
from threading import RLock
from hashlib import sha256

lock = RLock()
db, cursor = connect_mysql()


def get_user(username, password):
    sha256_password = sha256(password.encode()).hexdigest()

    try:
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        with lock:
            cursor.execute(query, (username, sha256_password))
            user = cursor.fetchone()
            if user:
                return user

    except Exception as e:
        print(f"[-] db Error : {e}")
        db.close()


def get_user_by_username(username):
    try:
        query = "SELECT * FROM users WHERE username = %s"
        with lock:
            cursor.execute(query, (username))
            user = cursor.fetchone()
            if user:
                return user

    except Exception as e:
        print(f"[-] db Error : {e}")
        db.close()


def register_user(username, password):
    sha256_password = sha256(password.encode()).hexdigest()

    try:
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        with lock:
            cursor.execute(query, (username, sha256_password))
            db.commit()

    except Exception as e:
        print(f"[-] db Error : {e}")
        db.rollback()
        db.close()


def search_sentences(keyword):
    try:
        query = "SELECT * FROM sentences WHERE sentence LIKE %s"
        with lock:
            cursor.execute(query, ("%" + keyword + "%"))
            sentences = cursor.fetchall()
            if sentences:
                return sentences

    except Exception as e:
        print(f"[-] db Error : {e}")
        db.close()
