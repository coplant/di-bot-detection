import sys
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

sys.path.append("..")

from config import BASE_DIR
from home.router import router as home_router

app = FastAPI()

app.mount("/static", StaticFiles(directory=BASE_DIR / "src" / "static"), name="static")

app.include_router(home_router)
