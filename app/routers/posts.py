from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Response
from schemas.post_schemas import PostBase, PostCreate, PostUpdate, Post
from database import get_db
from sqlalchemy.orm import Session
from typing import Union
import models
from uuid import uuid4

router = APIRouter()

@router.get("/get_post", response_model=list[PostBase])
def get_one_or_all_posts(*,post_id: Union[str, None]=None ,db: Session = Depends(get_db), status_code=200):
    if post_id:
        posts = db.query(models.Post).filter(models.Post.id == post_id).first()
        if not posts:
            raise HTTPException(status_code=404, detail="Post not found")
    posts = db.query(models.Post).all()
    return posts

@router.post("/create_post", response_model=PostCreate)
def create_post(*, post: PostCreate, db: Session = Depends(get_db)):
    check_post = db.query(models.Post).filter(models.Post.title == post.title).first()
    if check_post:
        raise HTTPException(status_code=400, detail="A post with this title already exists")
    
    db_post = models.Post(**post.dict())
    db_post.id = str(uuid4())    
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.put("/update_post/{post_id}", response_model=PostUpdate)
def update_post(*, post_id: str, post: PostUpdate, db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    db_post.title = post.title
    db_post.body = post.body
    db_post.published = post.published
    db.commit()
    db.refresh(db_post)
    return db_post

@router.delete("/delete_post/{post_id}")
def delete_post(*, post_id: str, db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(db_post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)