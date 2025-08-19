from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

with open('/flag', 'r') as f:
    FLAG = f.read()

class NoteCreate(BaseModel):
    title: str
    content: str

notes = {}
last_note_idx = -1

app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)
app = FastAPI()

def process_note_creation(note_create: NoteCreate):
    global last_note_idx
    global notes

    note = {'title': note_create.title, 'content': note_create.content}
    last_note_idx += 1
    notes[last_note_idx] = note
    return note

@app.post('/notes')
async def create_note(note_create: NoteCreate):
    return process_note_creation(note_create)

@app.get('/notes')
async def read_notes():
    return notes

@app.get('/admin')
async def get_admin(request: Request):      
    is_admin = request.headers.get('is-admin')
    if is_admin != 'true':
        return JSONResponse(status_code=401, content=None)
    return {'message': FLAG}
