from datetime import datetime, timedelta
from enum import Enum
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request
from starlette.responses import HTMLResponse, Response

from proxy.src.service import models
from proxy.src.config import EXPIRATION_TIME, STATIC_PATH


class Actions(Enum):
    FP_received = 0
    FP_analyzed = 1
    Cookie_sent = 2
    Cookie_received = 3
    Cookie_invalid = 4
    Bod_detected = 5


def generate_valid_until():
    valid_until = datetime.utcnow() + timedelta(seconds=EXPIRATION_TIME)
    return valid_until


def is_valid_uuid(client_uuid, version=4):
    try:
        uuid_obj = UUID(client_uuid, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == client_uuid


async def as_bot(request: Request, session: AsyncSession):
    user = models.User(ip=request.client.host, is_bot=True)
    session.add(user)
    await session.flush()
    log = models.Logging(user_id=user.id, action_id=Actions.Bod_detected.value)
    session.add(log)
    await session.commit()


async def is_valid_cookie(cookie: str, request: Request, session: AsyncSession):
    html_content = f"""<script type="module" src="{STATIC_PATH}"></script>"""
    if not cookie:
        return HTMLResponse(content=html_content, media_type="text/html")
    if not is_valid_uuid(cookie):
        await as_bot(request, session)
        return Response(status_code=status.HTTP_403_FORBIDDEN)
    else:
        query = select(models.Cookie).filter_by(value=cookie)
        result = await session.execute(query)
        result = result.unique().scalar_one_or_none()
        if not result:
            await as_bot(request, session)
            return Response(status_code=status.HTTP_403_FORBIDDEN)
        if not result.expiration_time >= datetime.utcnow():
            return HTMLResponse(content=html_content, media_type="text/html")
