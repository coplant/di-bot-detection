import sys
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.staticfiles import StaticFiles
from exceptions import validation_exception_handler

sys.path.append("..")

from config import BASE_DIR
from home.router import router as home_router

app = FastAPI()

app.mount("/static", StaticFiles(directory=BASE_DIR / "src" / "static"), name="static")
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.include_router(home_router)
