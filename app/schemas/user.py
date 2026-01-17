from pydantic import BaseModel, EmailStr,Field

class UserCreate(BaseModel):            #user sends the following data to us, so basically Incoming data
    name: str= Field(...,min_length = 1)
    email: EmailStr
    password: str = Field(..., min_length=6)
    age: int =Field(..., ge=5, le=100)
    job_role: str= Field(..., min_length=1)

class UserResponse(BaseModel):          # we send this back to the user ,so basically Outgoing Data
    id: int
    name: str
    email: EmailStr
    age: int
    job_role: str

class Config:
    orm_mode = True     # enables reading data from SQLAlchemy models

