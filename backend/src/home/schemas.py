from fastapi import Form
from pydantic import BaseModel


class FormData(BaseModel):
    username: str
    email: str
    code: str
    flag: bool

    @classmethod
    def as_form(cls,
                username: str = Form(...),
                email: str = Form(...),
                code: str = Form(...),
                flag: bool = Form(...)):
        return cls(username=username,
                   email=email, code=code,
                   flag=flag)
