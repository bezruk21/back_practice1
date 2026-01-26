from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import timedelta
from app.jwt import ACCESS_EXPIRES, REFRESH_EXPIRES

class Token(BaseModel):
    access_token: str
    access_token_expires: timedelta = ACCESS_EXPIRES

class TokenData(BaseModel):
    email: Optional[str] = None