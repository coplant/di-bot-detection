import sys
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.staticfiles import StaticFiles

from backend.src.exceptions import validation_exception_handler
from backend.src.config import BASE_DIR
from backend.src.home.router import router as home_router

app = FastAPI()

app.mount("/static", StaticFiles(directory=BASE_DIR / "src" / "static"), name="static")
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.include_router(home_router)
