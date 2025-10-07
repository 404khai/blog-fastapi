from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app import models, schemas, database

router = APIRouter(prefix="/comments", tags=["Comments"])

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ➕ Create a new comment
@router.post("/new", response_model=schemas.CommentResponse)
def add_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(models.Users).filter(models.Users.id == comment.ownerId).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if post exists
    post = db.query(models.Posts).filter(models.Posts.id == comment.postId).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    new_comment = models.Comments(
        comment=comment.comment,
        ownerId=comment.ownerId,
        postId=comment.postId,
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment



# 👤 Get all comments made by a specific user
@router.get("/user/{ownerId}", response_model=list[schemas.CommentResponse])
def get_user_comments(ownerId: int, db: Session = Depends(get_db)):
    comments = (
        db.query(models.Comments)
        .options(joinedload(models.Comments.post).joinedload(models.Posts.owner))
        .filter(models.Comments.ownerId == ownerId)
        .all()
    )
    if not comments:
        raise HTTPException(status_code=404, detail="No comments found for this user")
    return comments



#Get ALL Comments under a specific post
@router.get("/post/{postId}", response_model=list[schemas.CommentResponse])
def get_post_comments(postId: int, db: Session = Depends(get_db)):
    comments = (
        db.query(models.Comments)
        .filter(models.Comments.postId == postId)
        .all()
    )
    if not comments:
        raise HTTPException(status_code=404, detail="No comments found for this post")
    return comments



# ❌ Delete a comment
@router.delete("/{commentId}")
def delete_comment(commentId: int, db: Session = Depends(get_db)):
    comment = db.query(models.Comments).filter(models.Comments.id == commentId).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    db.delete(comment)
    db.commit()
    return {"message": "Comment deleted successfully"}
