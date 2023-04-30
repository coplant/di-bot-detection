import uuid

from sqlalchemy import Integer, Column, String, Boolean, ForeignKey, UUID
from backend.src.database import Base


class User(Base):
    __tablename__ = "users"
    id: int = Column(Integer, primary_key=True)
    uid: uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
    username: str = Column(String, nullable=False)
    email: str = Column(String, nullable=False, unique=True)
    code_id: int = Column(Integer, ForeignKey("codes.id"))
    is_active: bool = Column(Boolean, default=True)


class Code(Base):
    __tablename__ = "codes"
    id: int = Column(Integer, primary_key=True)
    code: str = Column(String, nullable=False, unique=True)
    is_active: bool = Column(Boolean, default=True)
