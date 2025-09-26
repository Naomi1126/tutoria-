from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None

class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None = None
    is_active: bool

    class Config:
        from_attributes = True  # para leer desde SQLAlchemy

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginData(BaseModel):
    email: EmailStr
    password: str
