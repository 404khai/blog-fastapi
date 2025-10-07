from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database

router = APIRouter(prefix="/comments", tags=["Comments"])

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

#New Comment
@router.post("/new", response_model=schemas.CommentResponse)
def addComment(comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(models.Users).filter(models.Users.id == comment.ownerId).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if post exists
    post = db.query(models.Posts).filter(models.Posts.id == comment.postId).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    newComment = models.Comments(
        comment=comment.comment,
        ownerId=comment.ownerId,
        postId=comment.postId,
    )
    db.add(newComment)
    db.commit()
    db.refresh(newComment)
    return newComment

#Get All Comments of a User
@router.get("/{ownerId}", response_model=list[schemas.CommentResponse])
def getUserComments(ownerId: int, db: Session = Depends(get_db)):
    comments = db.query(models.Comments).filter(models.Comments.ownerId == ownerId).all()
    return comments

#Get All Comments under a Post
@router.get("/{postId}", response_model=list[schemas.CommentResponse])
def getPostComments(postId: int, db: Session = Depends(get_db)):
    comments = db.query(models.Comments).filter(models.Comments.post_id == postId).all()
    return comments


#Delete a Comment
@router.delete("/{commentId}")
def deleteComment(commentId: int, db: Session = Depends(get_db)):
    comment = db.query(models.Comments).filter(models.Comments.id == commentId).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    db.delete(comment)
    db.commit()
    return {"message": "Comment deleted successfully"}
