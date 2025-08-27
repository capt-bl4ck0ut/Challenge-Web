from app.models import Post
from app.components import get_db

def get_posts():
    db = get_db()
    return db.session.execute(db.select(Post)).scalars().all()


def get_post(post_id):
    db = get_db()
    return db.session.execute(db.select(Post).where(Post.id == post_id)).scalars().first()


def add_post(title, content, author_id):
    db = get_db()
    db.session.add(Post(title=title, content=content, author_id=author_id))
    db.session.commit()


def remove_post(post_id):
    db = get_db()
    db.session.execute(db.delete(Post).where(Post.id == post_id))
    db.session.commit()


def hide_post(post_id):
    db = get_db()
    post = db.session.execute(db.select(Post).where(Post.id == post_id)).scalars().first()
    post.hidden = True
    db.session.commit()


def unhide_post(post_id):
    db = get_db()
    post = db.session.execute(db.select(Post).where(Post.id == post_id)).scalars().first()
    post.hidden = False
    db.session.commit()
