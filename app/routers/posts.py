from fastapi import APIRouter, Depends, HTTPException, status, Response
from schemas.post_schemas import PostBase, PostCreate, PostUpdate
from database import get_db
from sqlalchemy.orm import Session
import models
import uuid

router = APIRouter()

@router.get("/get_all_post", response_model=list[PostBase])
def get_all_posts(db: Session = Depends(get_db), status_code=200):
    posts = db.query(models.Post).all()
    return posts

@router.get("/get_one_post/{post_id}", response_model=PostBase)
def get_one_post(*, post_id: uuid.UUID, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.post("/create_post", response_model=PostBase)
def create_post(*, post: PostCreate, db: Session = Depends(get_db)):
    check_post = db.query(models.Post).filter(models.Post.title == post.title).first()
    if check_post:
        raise HTTPException(status_code=400, detail="A post with this title already exists")
    
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.put("/update_post/{post_id}", response_model=PostUpdate)
def update_post(*, post_id: str, post: PostUpdate, db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.title:
        db_post.title = post.title
    if post.body:
        db_post.body = post.body
    if post.published:
        db_post.published = post.published
    db.commit()
    db.refresh(db_post)
    return db_post

@router.delete("/delete_post/{post_id}")
def delete_post(post_id: uuid.UUID, db: Session = Depends(get_db), status_code=status.HTTP_200_OK):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(db_post)
    db.commit()
    return {"message": f"post {db_post.title} deleted successfully!"}