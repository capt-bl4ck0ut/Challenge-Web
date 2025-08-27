from random import choices
from string import digits
from app.models import ApiToken, ModelConstants
from app.components import get_db


def create_token(user_id):
    token = ''.join(choices(digits, k=ModelConstants.api_token_length))
    db = get_db()
    token = ApiToken(token=token, user_id=user_id, is_admin=(user_id == 1))
    db.session.add(token)
    db.session.commit()
    return token.token


def validate_token(token):
    db = get_db()
    token = db.session.execute(db.select(ApiToken).where(ApiToken.token == token)).scalars().first()
    return token != None


def validate_token_admin(token):
    db = get_db()
    token = db.session.execute(db.select(ApiToken).where(ApiToken.token == token)).scalars().first()
    return token != None and token.is_admin


def get_token(token):
    db = get_db()
    return db.session.execute(db.select(ApiToken).where(ApiToken.token == token)).scalars().first()


def remove_token(token):
    db = get_db()
    db.session.execute(db.delete(ApiToken).where(ApiToken.token == token))
    db.session.commit()
