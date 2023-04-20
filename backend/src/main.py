from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from config import BASE_DIR
from src.home.router import router as home_router

app = FastAPI()

app.mount("/static", StaticFiles(directory=BASE_DIR / "src" / "static"), name="static")

app.include_router(home_router)
