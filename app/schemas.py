from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
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
    ownerId: int


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    ownerId: int

    class Config:
        orm_mode = True



class CommentCreate(BaseModel):
    comment: str
    dateCreated: datetime
    ownerId: int


class CommentResponse(BaseModel):
    id: int
    dateCreated: datetime
    comment: str
    ownerId: int

    class Config:
        orm_mode = True

