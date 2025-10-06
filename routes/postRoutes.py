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


@router.post("/", response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # Check if the owner exists
    user = db.query(models.Users).filter(models.Users.id == post.owner_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_post = models.Posts(title=post.title, content=post.content, owner_id=post.owner_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/", response_model=list[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    return db.query(models.Posts).all()


@router.get("/{post_id}", response_model=schemas.PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Posts).filter(models.Posts.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Posts).filter(models.Posts.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return {"message": "Post deleted successfully"}
