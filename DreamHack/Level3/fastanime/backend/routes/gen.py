import asyncio
import aiohttp
from fastapi import APIRouter, Cookie, HTTPException
from ..config import settings

router = APIRouter()

@router.post("/api/gen")
async def gen(count: int, url: str):
    URL = url
    
    async def fetch_image():
        async with aiohttp.ClientSession() as session:
            async with session.get(URL, headers={"access-key":settings.get("SECRET_KEY")}) as response:
                data = await response.json()
                return data['images']
    
    # Make all requests concurrently
    tasks = [fetch_image() for _ in range(count)]
    results = await asyncio.gather(*tasks)
    
    return {"m": results}