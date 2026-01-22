# app/schemas/auth.py
from pydantic import BaseModel, EmailStr, Field

class LoginRequest(BaseModel):
    #Request schema for user login.
    email: EmailStr
    password: str = Field(..., min_length=6)

class TokenResponse(BaseModel):
    #Response schema for successful login.
    access_token: str
    token_type: str = "bearer"
