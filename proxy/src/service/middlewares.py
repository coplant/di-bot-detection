from fastapi import Request, status
from fastapi.responses import Response
from sqlalchemy import select

from database import async_session_maker
from service.models import User


async def validate_ip(request: Request, call_next):
    client_ip = str(request.client.host)
    async with async_session_maker() as session:
        query = select(User).filter_by(ip=client_ip).filter_by(is_bot=True)
        result = await session.execute(query)
        result = result.scalars().all()
    if client_ip in [user.ip for user in result]:
        return Response(status_code=status.HTTP_403_FORBIDDEN)
    return await call_next(request)
