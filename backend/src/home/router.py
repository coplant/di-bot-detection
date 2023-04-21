from fastapi import APIRouter, Form, Depends
from fastapi.templating import Jinja2Templates
from starlette import status
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

from config import BASE_DIR
from home.schemas import FormData

router = APIRouter()
templates = Jinja2Templates(directory=BASE_DIR / "src" / "templates")


@router.get("/", response_class=HTMLResponse, responses={422: {"model": ""}})
async def root(request: Request):
    return templates.TemplateResponse("index.html",
                                      {"request": request, "submit_form": router.url_path_for("submit_form")})


@router.post("/submit", responses={422: {"model": ""}})
async def submit_form(form_data: FormData = Depends(FormData.as_form)):
    # todo: data proccessing
    return RedirectResponse(url="/thanks", status_code=status.HTTP_302_FOUND)


@router.get("/thanks", response_class=HTMLResponse)
async def thanks(request: Request):
    return templates.TemplateResponse("thanks.html", {"request": request})
