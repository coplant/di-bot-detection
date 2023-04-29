import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

from config import BASE_DIR
from database import get_async_session
from home.models import User, Code
from home.schemas import FormData
from home.utils import get_code

router = APIRouter()
templates = Jinja2Templates(directory=BASE_DIR / "src" / "templates")


@router.get("/", response_class=HTMLResponse, responses={422: {"model": ""}})
async def root(request: Request,
               session: AsyncSession = Depends(get_async_session)):
    cookies = request.cookies
    user_identifier = cookies.get("userIdentifier")
    query = select(User).filter_by(uid=user_identifier)
    user = await session.execute(query)
    user = user.unique().scalar_one_or_none()
    if not user:
        response = templates.TemplateResponse("index.html",
                                              {"request": request, "submit_form": router.url_path_for("submit_form")})
    else:
        response = RedirectResponse(url="/thanks", status_code=status.HTTP_302_FOUND)
    return response


@router.post("/submit", responses={422: {"model": ""}})
async def submit_form(form_data: FormData = Depends(FormData.as_form),
                      session: AsyncSession = Depends(get_async_session)):
    try:
        code: Code = await get_code(form_data, session)
        if code:
            try:
                code.is_active = False
                user = User(username=form_data.username, email=form_data.email, code_id=code.id)
                session.add(user)
                await session.flush()
            except Exception:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
            else:
                await session.commit()
                response = RedirectResponse(url="/thanks", status_code=status.HTTP_302_FOUND)
                response.set_cookie(key="userIdentifier", value=user.uid, max_age=999999999,
                                    expires=datetime.datetime(2030, 1, 1).isoformat() + 'Z')
        else:
            response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        return response
    except HTTPException as e:
        return Response(content=e.detail, status_code=e.status_code)
    except ValidationError:
        return RedirectResponse(url="/", status_code=status.HTTP_400_BAD_REQUEST)


@router.get("/thanks", response_class=HTMLResponse)
async def thanks(request: Request,
                 session: AsyncSession = Depends(get_async_session)):
    cookies = request.cookies
    user_identifier = cookies.get("userIdentifier")
    query = select(User).filter_by(uid=user_identifier)
    user = await session.execute(query)
    user = user.unique().scalar_one_or_none()
    if user:
        response = templates.TemplateResponse("thanks.html", {"request": request, "id": user.id})
    else:
        response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    return response


@router.get("/noscript", response_class=HTMLResponse)
async def noscript(request: Request):
    return templates.TemplateResponse("nojs.html", {"request": request})
