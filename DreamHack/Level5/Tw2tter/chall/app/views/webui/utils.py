from dataclasses import dataclass, fields
from functools import wraps
from flask import render_template, session, redirect
from app.components.post import get_post as get_post_from_db, get_posts as get_posts_from_db


def render_template_wrapper(template, **kwargs):
    return render_template(template, authenticated=session.get('authenticated'), **kwargs)


def require_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('authenticated'):
            return func(*args, **kwargs)
        else:
            return redirect('/auth/login')
    return wrapper


def require_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('authenticated') and is_admin(session):
            return func(*args, **kwargs)
        else:
            return redirect('/auth/login')
    return wrapper


@dataclass
class Permission:
    # None: Any
    read: bool = False
    # None: Any
    write: bool = False

    def __le__(self, other):
        assert isinstance(other, Permission)
        # True <= False
        def le(elem1, elem2):
            return elem2 is False or elem1 == elem2
        return all(
            le(getattr(self, field.name), getattr(other, field.name))
            for field in fields(self)
        )


def is_admin(session):
    return session.get('user_id') == 1

def permission_for_post(session, post):
    permission = Permission()
    user_id = session.get('user_id')
    if is_admin(session) or user_id == post.author_id or not post.hidden:
        permission.read = True
    if is_admin(session) or user_id == post.author_id:
        permission.write = True
    return permission

def get_post(session, post_id, permission=Permission()):
    post = get_post_from_db(post_id)
    if post != None and permission_for_post(session, post) <= permission:
        return post
    else:
        return None

def get_posts(session, permission=Permission()):
    posts = get_posts_from_db()
    return filter(lambda post: permission_for_post(session, post) <= permission, posts)
