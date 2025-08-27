from app.models import User
from app.components import get_db


def get_users():
    db = get_db()
    return db.session.execute(db.select(User)).scalars().all()


def get_user(user_id):
    db = get_db()
    return db.session.execute(db.select(User).where(User.id == user_id)).scalars().first()


def get_user_by_username_and_password(username, password):
    db = get_db()
    return db.session.execute(db.select(User).where(User.username == username).where(User.password == password)).scalars().first()


def add_user(username, password):
    db = get_db()
    db.session.add(User(username=username, password=password))
    db.session.commit()
