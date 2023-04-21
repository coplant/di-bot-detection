from fastapi import APIRouter, Form, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

from config import BASE_DIR
from database import get_async_session
from home.schemas import FormData
from home.utils import use_code

router = APIRouter()
templates = Jinja2Templates(directory=BASE_DIR / "src" / "templates")


@router.get("/", response_class=HTMLResponse, responses={422: {"model": ""}})
async def root(request: Request):
    # todo: check cookie
    condition = True
    if condition:
        response = templates.TemplateResponse("index.html",
                                              {"request": request, "submit_form": router.url_path_for("submit_form")})
    else:
        response = RedirectResponse(url="/thanks", status_code=status.HTTP_302_FOUND)
    return response


@router.post("/submit", responses={422: {"model": ""}})
async def submit_form(form_data: FormData = Depends(FormData.as_form),
                      session: AsyncSession = Depends(get_async_session)):
    try:
        # todo: data processing
        if await use_code(form_data, session):
            # todo: set cookie
            response = RedirectResponse(url="/thanks", status_code=status.HTTP_302_FOUND)
        else:
            response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        return response
    except ValidationError as e:
        raise HTTPException(status_code=422)


@router.get("/thanks", response_class=HTMLResponse)
async def thanks(request: Request):
    # todo: if id in cookie:
    condition = True
    if condition:
        response = templates.TemplateResponse("thanks.html", {"request": request, "id": 0})
    else:
        response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    return response
