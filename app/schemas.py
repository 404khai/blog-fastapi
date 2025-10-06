from pydantic import BaseModel, EmailStr
from typing import List, Optional


# ----- USER 
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True


# ----- POST 
class PostCreate(BaseModel):
    title: str
    content: str
    owner_id: int


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int

    class Config:
        orm_mode = True



