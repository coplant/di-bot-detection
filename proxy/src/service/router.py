import httpx as httpx
from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import Response

router = APIRouter()

API_HOST = "localhost"
PORT = 8000


@router.api_route("/", methods=["GET", "POST"])
@router.api_route("/{route_path:path}", methods=["GET", "POST"])
async def proxy_route(request: Request):
    body = await request.body()
    payload = dict(await request.form())
    async with httpx.AsyncClient() as client:
        headers = {k.decode(): v.decode() for k, v in request.headers.raw if
                   k.decode().lower() in ('content-type', 'host')}
        # headers["host"] = API_HOST
        proxy_request = client.build_request(
            method=request.method,
            url=str(request.url.replace(hostname=API_HOST, port=PORT)),
            headers=headers,
            content=body,
            data=payload,
            cookies=request.cookies
        )
        response = await client.send(proxy_request, follow_redirects=True)
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = {k.decode(): v.decode() for k, v in response.headers.raw if k.decode().lower() not in excluded_headers}
    response = Response(content=response.content, status_code=response.status_code, headers=headers)
    return response
