from sqlalchemy import Integer, Column, String, Boolean
from src.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    uid = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    code = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, default=True)


class Code(Base):
    __tablename__ = "codes"
    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
