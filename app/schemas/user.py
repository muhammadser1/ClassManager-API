from datetime import date

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    name: str
    password: str


class SignupRequest(BaseModel):
    name: str
    email: str
    password: str
    birthday: date

class ResetPasswordRequest(BaseModel):
    token: str
    password: str


class SuggestionRequest(BaseModel):
    username: str
    email: EmailStr
    msg: str



class SupportRequest(BaseModel):
    username: str
    email: EmailStr
    msg: str