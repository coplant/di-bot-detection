import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, UUID, Boolean, JSON, String, TIMESTAMP, ForeignKey, DateTime
from sqlalchemy.sql import sqltypes

from src.database import Base
from service.utils import generate_valid_until


class User(Base):
    __tablename__ = "users"
    id: int = Column(Integer, primary_key=True)
    uid: uuid = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4)
    ip: str = Column(String, nullable=False)
    fingerprint: sqltypes.JSON = Column(JSON)
    timestamp: datetime = Column(TIMESTAMP, default=datetime.utcnow)
    is_bot: bool = Column(Boolean, nullable=False, default=False)


class Cookie(Base):
    __tablename__ = "cookies"
    id: int = Column(Integer, primary_key=True)
    value: uuid = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4)
    timestamp: datetime = Column(TIMESTAMP, default=datetime.utcnow)
    expiration_time: datetime = Column(DateTime, default=generate_valid_until)
    user_id: int = Column(Integer, ForeignKey("users.id"))
    is_active: bool = Column(Boolean, default=True)


class Action(Base):
    __tablename__ = "actions"
    id: int = Column(Integer, primary_key=True)
    value: str = Column(String)


class Logging(Base):
    __tablename__ = "logging"
    id: int = Column(Integer, primary_key=True)
    timestamp: datetime = Column(TIMESTAMP, default=datetime.utcnow)
    user_id: int = Column(Integer, ForeignKey("users.id"))
    cookie_id: int = Column(Integer, ForeignKey("cookies.id"))
    action_id: int = Column(Integer, ForeignKey("actions.id"))
