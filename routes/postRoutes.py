from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database

router = APIRouter(prefix="/posts", tags=["Posts"])

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Create Post
@router.post("/new", response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # Check if the owner exists
    user = db.query(models.Users).filter(models.Users.id == post.ownerId).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_post = models.Posts(title=post.title, content=post.content, ownerId=post.ownerId)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#Get All posts
@router.get("/all", response_model=list[schemas.PostResponse])
def getAllPosts(db: Session = Depends(get_db)):
    return db.query(models.Posts).all()


# Get all posts of a specific user
@router.get("/{ownerId}/posts", response_model=list[schemas.PostResponse])
def get_user_posts(ownerId: int, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(models.Users).filter(models.Users.id == ownerId).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Fetch all posts belonging to that user
    posts = db.query(models.Posts).filter(models.Posts.ownerId == ownerId).all()
    return posts


@router.get("/{postId}", response_model=schemas.PostResponse)
def get_post(postId: int, db: Session = Depends(get_db)):
    #Does post exist
    post = db.query(models.Posts).filter(models.Posts.id == postId).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.delete("/{postId}")
def delete_post(postId: int, db: Session = Depends(get_db)):
    post = db.query(models.Posts).filter(models.Posts.id == postId).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return {"message": "Post deleted successfully"}
