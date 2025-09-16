from pydantic import BaseModel, EmailStr


class SUserAuth(BaseModel):
    email: EmailStr
    password: str


class SToken(BaseModel):
    access_token: str
    refresh_token: str
