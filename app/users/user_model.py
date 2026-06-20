from pydantic import BaseModel, Field
from enum import Enum

class GharRole(str, Enum):
    HEAD = "head"       # Ghar ka bada
    MEMBER = "member"   # Ghar ke baqi log

class UserRegister(BaseModel):
    # EmailStr hata kar simple str lagaya aur validation tight ki
    username: str = Field(
        ..., 
        min_length=3, 
        max_length=20, 
        pattern=r"^[a-zA-Z0-9_]+$", 
        description="Username sirf akshar, number aur underscore ho sakta hai (no spaces)"
    )
    full_name: str = Field(..., min_length=2, max_length=50)
    password: str = Field(..., min_length=6)
    role: GharRole = GharRole.MEMBER

    class Config:
        str_strip_whitespace = True