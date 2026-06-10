from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    token: str
    user: dict[str, str | int]


class AnalyzeRequest(BaseModel):
    address: str


class AnalyzeResponse(BaseModel):
    analysis_id: int

