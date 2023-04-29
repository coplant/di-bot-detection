import requests
from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import Response

router = APIRouter()

API_HOST = "localhost"
PORT = "8000"


@router.api_route("/", methods=["GET", "POST"])
@router.api_route("/{path}", methods=["GET", "POST"])
async def proxy_route(request: Request):
    data = await request.body()
    payload = dict(await request.form())
    res = requests.request(
        method=request.method,
        url=str(request.url.replace(hostname=API_HOST, port=PORT)),
        headers={k.decode(): v.decode() for k, v in request.headers.raw if
                 k.decode().lower() in ('host', 'content-type')},
        data=data,
        json=payload,
        cookies=request.cookies,
        allow_redirects=False,
    )
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = {k: v for k, v in res.raw.headers.items() if k.lower() not in excluded_headers}
    response = Response(content=res.content, status_code=res.status_code, headers=headers)
    return response
