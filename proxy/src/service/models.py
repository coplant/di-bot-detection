import ipaddress
import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, UUID, Boolean, JSON, String, TIMESTAMP
from sqlalchemy.sql import sqltypes

from src.database import Base


class User(Base):
    __tablename__ = "users"
    id: int = Column(Integer, primary_key=True)
    uid: uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
    ip: str = Column(String, nullable=False)
    fingerprint: sqltypes.JSON = Column(JSON)
    timestamp: datetime = Column(TIMESTAMP, default=datetime.utcnow)
    is_bot: bool = Column(Boolean, nullable=False, default=False)
