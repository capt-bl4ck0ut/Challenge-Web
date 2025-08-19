from fastapi import APIRouter, Response, HTTPException
from ..config import settings
from pydantic import BaseModel
import jwt

router = APIRouter()

users = {
    "admin":settings.get("ADMIN_PASSWORD"),
    "guest":"guest"
}

class LoginParams(BaseModel):
    username: str
    password: str
    
class Register(BaseModel):
    username: str
    password: str
    
@router.post("/api/login")
async def root(p: LoginParams, response: Response):
    username = p.username
    password = p.password
    if (username not in users):
        raise HTTPException(status_code=400, detail="User not found")
    if (users[username] != password):
        raise HTTPException(status_code=400, detail="Wrong password")
    token = jwt.encode({"username":username}, settings.get("SECRET_KEY"), algorithm="HS256")
    response.set_cookie(
        key="token",
        value=token,
        httponly=True,
        max_age=3600 
    )
    return {"detail": "Login successfully"}

@router.post("/api/register")
async def root(p: LoginParams, response: Response):
    username = p.username
    password = p.password
    if (username in users):
        raise HTTPException(status_code=400, detail="User exists")
    users[username] = password
    token = jwt.encode({"username":username}, settings.get("SECRET_KEY"), algorithm="HS256")
    response.set_cookie(
        key="token",
        value=token,
        httponly=True,
        max_age=3600 
    )
    return {"detail": "Register successfully"}