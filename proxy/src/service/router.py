import asyncio

import httpx as httpx
from celery.result import AsyncResult
from fastapi import APIRouter
from starlette import status
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse, HTMLResponse

from proxy.src.ratelimiter import limiter
from proxy.src.service.schemas import FingerprintSchema
from proxy.src.assessment.background import analyze_fingerprint
from proxy.src.config import API_HOST, API_PORT, RATE_LIMITER_TIME, RATE_LIMITER_COUNT

router = APIRouter()


@router.get("/api/{task_id}")
async def get_fingerprint(task_id: str):
    async_result = AsyncResult(task_id)
    while async_result.state != 'SUCCESS':
        await asyncio.sleep(0.5)
    response = RedirectResponse(url="/", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    response.set_cookie(key="sessionIdentifier", value=async_result.result)
    return response


@router.post("/api")
async def get_fingerprint(request: Request, fingerprint: FingerprintSchema):
    if fingerprint:
        result = analyze_fingerprint.delay(fingerprint.dict(), request.headers.get("X-Forwarded-For"))
        if result:
            return RedirectResponse(url=f"/api/{result}", status_code=status.HTTP_302_FOUND)
    return Response(status_code=status.HTTP_403_FORBIDDEN)


@router.api_route("/", methods=["GET", "POST"])
@router.api_route("/{route_path:path}", methods=["GET", "POST"])
@limiter.limit(f"{RATE_LIMITER_COUNT}/{RATE_LIMITER_TIME}seconds")
async def proxy_route(request: Request):
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
    response = HTMLResponse(content=response.content, status_code=response.status_code, headers=headers)
    return response
