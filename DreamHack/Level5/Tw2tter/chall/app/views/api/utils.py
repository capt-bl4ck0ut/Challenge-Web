from dataclasses import asdict, dataclass, fields
from functools import wraps
import json
from flask import Response, request
from app.components.post import get_post as get_post_from_db, get_posts as get_posts_from_db


@dataclass
class ApiResponse:
    success: bool
    data: dict

    def __dict__(self):
        return asdict(self)
    
    def json(self):
        return json.dumps(self.__dict__())
    
def fail():
    raise Exception


def require_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.form.get('token'):
            return func(*args, **kwargs)
        else:
            return ApiResponse(False, {}).json()
    return wrapper


def json_response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            r = func(*args, **kwargs)
            if r is None:
                r = ApiResponse(False, {}).json()
        except Exception:
            r = ApiResponse(False, {}).json()
        return Response(r, mimetype='application/json')
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

def is_admin(api_token):
    return api_token.is_admin

def permission_for_post(api_token, post):
    permission = Permission()
    if api_token.is_admin or api_token.user_id == post.author_id or not post.hidden:
        permission.read = True
    if api_token.is_admin or api_token.user_id == post.author_id:
        permission.write = True
    return permission


def get_post(api_token, post_id, permission=Permission()):
    post = get_post_from_db(post_id)
    if post != None and permission_for_post(api_token, post) <= permission:
        return post
    else:
        return None

def get_posts(api_token, permission=Permission()):
    posts = get_posts_from_db()
    return filter(lambda post: permission_for_post(api_token, post) <= permission, posts)
