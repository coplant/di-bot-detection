import json

import httpx as httpx
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request
from starlette.responses import Response
from ratelimiter import limiter

from proxy.src.database import get_async_session
from proxy.src.config import API_HOST, API_PORT, RATE_LIMITER_TIME, RATE_LIMITER_COUNT
from proxy.src.service.schemas import FingerprintSchema
from proxy.src.service.utils import is_valid_cookie

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
    not_valid = await is_valid_cookie(cookie, request, session)
    if not_valid:
        return not_valid
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
