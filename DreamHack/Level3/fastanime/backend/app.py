from fastapi import FastAPI
from .routes import default, auth, gen
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(default.router)
app.include_router(auth.router)
app.include_router(gen.router)