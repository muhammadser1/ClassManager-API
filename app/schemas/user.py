from pydantic import BaseModel


class LoginRequest(BaseModel):
    name: str
    password: str


class SignupRequest(BaseModel):
    name: str
    email: str
    password: str


class ResetPasswordRequest(BaseModel):
    token: str
    password: str
