from fastapi import APIRouter, Cookie, HTTPException
from ..config import settings
import jwt

router = APIRouter()

@router.post("/api")
async def root():
    return {"message": "This is FastAPI backend"}

@router.post("/api/debug")
async def debug(filename: str, mode: bool = False, permission: bool = False, token: str = Cookie(default=None)):
    if (token == None):
        raise HTTPException(status_code=400, detail="No token provided")
    try:
        payload = jwt.decode(token, settings.get("SECRET_KEY"), algorithms="HS256")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to decode token")
    if (payload['username'] != 'admin'):
        raise HTTPException(status_code=400, detail="Admin only")
    if (mode == False or permission == False):
        raise HTTPException(status_code=400, detail="You don't have permission to do this")
    return open(filename).read()