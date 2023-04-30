import httpx as httpx
from fastapi import APIRouter, Body
from starlette.requests import Request
from starlette.responses import Response, HTMLResponse
from proxy.src.config import API_HOST, API_PORT

router = APIRouter()
STATIC_PATH = "/static/js/core.js"


@router.post("/api/json")
async def get_fingerprint():
    # todo: receive fingerprint
    return NotImplemented


@router.api_route("/", methods=["GET", "POST"])
@router.api_route("/{route_path:path}", methods=["GET", "POST"])
async def proxy_route(request: Request):
    cookie = request.cookies.get("sessionIdentifier")
    if not cookie:
        html_content = f"""<script type="module" src="{STATIC_PATH}"></script>"""
        return HTMLResponse(content=html_content, media_type="text/html")

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
