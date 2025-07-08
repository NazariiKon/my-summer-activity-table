from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.router import main_router

app = FastAPI()
app.include_router(main_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Или "*" для всех
    allow_methods=["GET", "POST"],
)