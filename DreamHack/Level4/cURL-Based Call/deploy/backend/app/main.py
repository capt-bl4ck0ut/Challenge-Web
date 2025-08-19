import os
from datetime import datetime
from fastapi import FastAPI, Response, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

with open('/flag', 'r') as f:
    FLAG = f.read()

class Post(BaseModel):
    idx: int
    title: str
    content: str
    author: str
    created_at: datetime
    updated_at: datetime

class PostCreate(BaseModel):
    title: str
    content: str
    author: str

class PostUpdatePut(BaseModel):
    title: str
    content: str
    author : str

class PostUpdatePatch(BaseModel):
    title: str | None = None
    content: str | None = None
    author : str | None = None


simple_tokens = []
posts = {}
next_post_idx = 0

app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)


def process_post_creation(post_create: PostCreate):
    global next_post_idx
    global posts
    post = Post(
        idx=next_post_idx,
        title=post_create.title,
        content=post_create.content,
        author=post_create.author,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    posts[next_post_idx] = post
    next_post_idx += 1
    return post

def process_post_full_update(post_idx, post_update_put: PostUpdatePut):
    global posts
    post = posts[post_idx]
    post.title = post_update_put.title
    post.content = post_update_put.content
    post.author = post_update_put.author
    post.updated_at = datetime.now()
    return post

def process_post_partial_update(post_idx, post_update_patch: PostUpdatePatch):
    global posts
    post = posts[post_idx]
    if post_update_patch.title:
        post.title = post_update_patch.title
    if post_update_patch.content:
        post.content = post_update_patch.content
    if post_update_patch.author:
        post.author = post_update_patch.author
    post.updated_at = datetime.now()
    return post


@app.middleware('http')
async def verify_user(request: Request, call_next):
    if request.url.path != '/auth':
        if request.headers.get('Simple-Token') not in simple_tokens:
            return JSONResponse(status_code=401, content=None)
    response = await call_next(request)
    return response

@app.post('/auth')
async def issue_token():
    global simple_tokens
    simple_token = os.urandom(32).hex()
    simple_tokens.append(simple_token)
    return simple_token

@app.post('/posts')
async def create_post(post_create: PostCreate):
    return process_post_creation(post_create)

@app.get('/posts')
async def read_posts():
    return posts

@app.get('/posts/{post_idx}')
async def read_posts_by_post_idx(post_idx: int, response: Response):
    if post_idx in posts:
        return posts[post_idx]
    response.status_code = 404
    return None

@app.put('/posts/{post_idx}')
async def update_post_put(post_idx: int, post_update_put: PostUpdatePut, response: Response):
    global posts
    if post_idx in posts:
        return process_post_full_update(post_idx, post_update_put)
    response.status_code = 404
    return None

@app.delete('/posts/{post_idx}')
async def delete_post(post_idx: int, response: Response):
    global posts
    if post_idx in posts:
        del posts[post_idx]
        response.status_code = 204
        return None
    response.status_code = 404
    return None

@app.patch('/posts/{post_idx}')
async def update_post_patch(post_idx: int, post_update_patch: PostUpdatePatch, response: Response):
    global posts
    if post_idx in posts:
        return process_post_partial_update(post_idx, post_update_patch)
    response.status_code = 404
    return None

@app.get('/admin')
async def get_admin(request: Request):
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    if x_forwarded_for != '127.0.0.1':
        return JSONResponse(status_code=401, content=None)

    return {'message': FLAG}
