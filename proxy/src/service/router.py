import uuid
from datetime import datetime

import httpx as httpx
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request
from starlette.responses import Response, HTMLResponse
from ratelimiter import limiter

from database import get_async_session
from proxy.src.config import API_HOST, API_PORT, STATIC_PATH, RATE_LIMITER_TIME, RATE_LIMITER_COUNT
from service.models import Cookie, User
from service.schemas import FingerprintSchema
from service.utils import is_valid_uuid, as_bot

router = APIRouter()


@router.post("/api/json")
async def get_fingerprint(request: Request,
                          fingerprint: FingerprintSchema):
    # todo: receive fingerprint
    return NotImplemented


@router.api_route("/", methods=["GET", "POST"])
@router.api_route("/{route_path:path}", methods=["GET", "POST"])
@limiter.limit(f"{RATE_LIMITER_COUNT}/{RATE_LIMITER_TIME}seconds")
async def proxy_route(request: Request,
                      session: AsyncSession = Depends(get_async_session)):
    cookie = request.cookies.get("sessionIdentifier")
    html_content = f"""<script type="module" src="{STATIC_PATH}"></script>"""
    if not cookie:
        return HTMLResponse(content=html_content, media_type="text/html")
    if not is_valid_uuid(cookie):
        await as_bot(request, session)
        return Response(status_code=status.HTTP_403_FORBIDDEN)
    else:
        query = select(Cookie).filter_by(value=cookie)
        result = await session.execute(query)
        result = result.unique().scalar_one_or_none()
        if not result:
            await as_bot(request, session)
            return Response(status_code=status.HTTP_403_FORBIDDEN)
        if not result.expiration_time >= datetime.utcnow():
            return HTMLResponse(content=html_content, media_type="text/html")

    # todo: проверка на то, является ли юзер ботом или нет

    # todo: сделать разветвление
    #   1: если кук нет - рендерить HTML + JS,
    #       JS отправляет данные на роут,
    #       роут устанавливает куки
    #       куки сообщают о том, что пользователь отправил свои отпечатки => в JS делать редирект или обновление
    #   2: если есть куки - делать проксирование
    #       куки должны быстро истекать? живут до закрытия браузера
    #       в первом роуте делать запрос в DB по IP
    #       если кука не соответствует пользователю - запрос на получение отпечатков

    body = await request.body()
    payload = dict(await request.form())
    async with httpx.AsyncClient() as client:
        headers = {k.decode(): v.decode() for k, v in request.headers.raw if
                   k.decode().lower() in ('content-type',)}
        headers["host"] = API_HOST + f":{API_PORT}" if API_PORT else ""
        proxy_request = client.build_request(
            method=request.method,
            url=str(request.url.replace(hostname=API_HOST, port=API_PORT)),
            headers=headers,
            content=body,
            data=payload,
            cookies=request.cookies
        )
        response = await client.send(proxy_request, follow_redirects=False)
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = {k.decode(): v.decode() for k, v in response.headers.raw if k.decode().lower() not in excluded_headers}
    response = Response(content=response.content, status_code=response.status_code, headers=headers)
    return response
