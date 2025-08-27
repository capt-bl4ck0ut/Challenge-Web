import os
from flask import Flask
from app.views.webui.route import bp as bp_webui
from app.views.api.route import bp as bp_api
from app.models import db, Post, User

def init_db(app):
    try:
        os.remove('instance/database.db')
    except FileNotFoundError:
        pass
    with app.app_context():
        db = app.extensions['sqlalchemy']
        db.create_all()
        db.session.add(User(username='admin', password=os.environ.get('ADMIN_PASSWORD')))
        db.session.add(User(username='dream', password=os.urandom(8).hex()))
        db.session.add(User(username='guest', password='guest'))
        db.session.add(Post(title='I am admin user', content='Nice to meet you, 여러분. 나는 관리자 of Tw2tter. Epsilon Mask 입니다 😉', author_id=1))
        db.session.add(Post(title='이렇게 적으면 되나?', content=os.environ.get('FLAG'), author_id=2, hidden=True))
        db.session.add(Post(title='큰일 날 뻔 했네요', content='Tw2tter는 처음이라 아무거나 막 누르다가 개인정보를 업로드해버렸어요 😅😅 바로 글을 숨겼는데 그 사이에 본 사람은 없겠죠...??', author_id=2))
        db.session.add(Post(title='안녕하세요', content='여긴 정말 한적하네요', author_id=3))
        db.session.commit()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(32)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.register_blueprint(bp_webui)
    app.register_blueprint(bp_api)
    db.init_app(app)
    init_db(app)
    return app
