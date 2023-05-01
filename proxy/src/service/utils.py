from datetime import datetime, timedelta
from enum import Enum
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from service import models
from src.config import EXPIRATION_TIME


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
