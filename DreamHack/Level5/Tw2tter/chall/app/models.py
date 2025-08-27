from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


@dataclass
class ModelConstants:
    api_token_length: int = 6
    username_max_length: int = 30
    password_max_length: int = 100
    post_title_max_length: int = 40
    post_content_max_length: int = 300
    report_reason_max_length: int = 100


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(ModelConstants.username_max_length), unique=True, nullable=False)
    password = db.Column(db.String(ModelConstants.password_max_length), nullable=False)
    posts = db.relationship('Post', backref='author')


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(ModelConstants.post_title_max_length), nullable=False)
    content = db.Column(db.String(ModelConstants.post_content_max_length), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    hidden = db.Column(db.Boolean, nullable=False, default=False)


class Report(db.Model):
    __tablename__ = 'reports'
    id = db.Column(db.Integer, primary_key=True)
    reporter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    reason = db.Column(db.String(ModelConstants.report_reason_max_length), nullable=False)


class ApiToken(db.Model):
    __tablename__ = 'api_tokens'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(ModelConstants.api_token_length), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
