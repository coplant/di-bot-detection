from fastapi import Form
from pydantic import BaseModel, EmailStr


class FormData(BaseModel):
    username: str
    email: EmailStr
    code: str
    flag: bool

    @classmethod
    def as_form(cls,
                username: str = Form(...),
                email: EmailStr = Form(...),
                code: str = Form(...),
                flag: bool = Form(...)):
        return cls(username=username,
                   email=email, code=code,
                   flag=flag)
