from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    # 👇 Relationship: A user can have many posts
    posts = relationship("Posts", back_populates="owner")
    comments = relationship("Comments", back_populates="owner")


class Posts(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    ownerId = Column(Integer, ForeignKey("users.id"))
    postId = Column(Integer, ForeignKey("posts.id"))

    # Relationship back to the user
    owner = relationship("Users", back_populates="posts")



class Comments(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    comment = Column(String, nullable=False)
    dateCreated = Column(datetime, nullable=False)
    ownerId = Column(Integer, ForeignKey("users.id"))

    # Relationship back to the user
    owner = relationship("Users", back_populates="comments")