from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from config import BASE_DIR

router = APIRouter()
templates = Jinja2Templates(directory=BASE_DIR / "src" / "templates")


@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

# @router.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
