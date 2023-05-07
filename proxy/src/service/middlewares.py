from fastapi import Request, status
from fastapi.responses import Response
from sqlalchemy import select

from proxy.src.service.models import User
from proxy.src.database import async_session_maker
from proxy.src.service.utils import is_valid_cookie


async def validate_fingerprint(request: Request, call_next):
    if request.url.path.startswith(("/api", "/static")):
        return await call_next(request)
    else:
        cookie_value = request.cookies.get("sessionIdentifier")
        async with async_session_maker() as session:
            response, cookie = await is_valid_cookie(cookie_value, request, session)
            if response:
                return response
            query = select(User).filter_by(id=cookie.user_id)
            result = await session.execute(query)
            result = result.scalar_one_or_none()
            if result and result.is_bot:
                return Response(status_code=status.HTTP_403_FORBIDDEN)
        return await call_next(request)


async def validate_ip(request: Request, call_next):
    client_ip = request.headers.get("X-Forwarded-For")
    async with async_session_maker() as session:
        query = select(User).filter_by(ip=client_ip).filter_by(is_bot=True)
        result = await session.execute(query)
        result = result.scalars().all()
    if client_ip in [user.ip for user in result]:
        return Response(status_code=status.HTTP_403_FORBIDDEN)
    return await call_next(request)
