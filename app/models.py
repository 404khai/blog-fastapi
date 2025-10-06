from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    posts = relationship("Posts", back_populates="owner")
    comments = relationship("Comments", back_populates="owner")


class Posts(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    ownerId = Column(Integer, ForeignKey("users.id"))

    owner = relationship("Users", back_populates="posts")
    comments = relationship("Comments", back_populates="post")  # ✅ matches “post” in Comments


class Comments(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    comment = Column(String, nullable=False)
    dateCreated = Column(DateTime, default=datetime.utcnow, nullable=False)
    ownerId = Column(Integer, ForeignKey("users.id"))
    postId = Column(Integer, ForeignKey("posts.id"))  # ✅ corrected

    owner = relationship("Users", back_populates="comments")
    post = relationship("Posts", back_populates="comments")
