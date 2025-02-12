from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc


from database import SessionLocal
from table_user import User
from table_post import Post
from table_feed import Feed
from schema import UserGet, PostGet, FeedGet


app = FastAPI()

def get_db():
    with SessionLocal() as db:
        return db

@app.get("/user/{id}", response_model=UserGet)
def get_user(id: int, db: Session = Depends(get_db)):
    user =  db.query(User).filter(User.id == id).first()
    if user is None:
        raise HTTPException(404, "user not found")
    return UserGet.from_orm(user)

@app.get("/post/{id}", response_model=PostGet)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()
    if post is None:
        raise HTTPException(404, "post not found")
    return PostGet.from_orm(post)

@app.get("/user/{id}/feed", response_model=List[FeedGet])
def get_feed_by_user(id: int, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Feed).filter(Feed.user_id == id).order_by(Feed.time.desc()).limit(limit).all()

@app.get("/post/{id}/feed", response_model=List[FeedGet])
def get_feed_by_post(id: int, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Feed).filter(Feed.post_id == id).order_by(Feed.time.desc()).limit(limit).all()

@app.get("/post/recommendations/", response_model = List[PostGet])
def get_most_liked_posts(limit: int = 10, db: Session = Depends(get_db)):
   results = (
       db.query(Post)
       .join(Feed)
       .filter(Feed.action == 'like')
       .group_by(Post.id)
       .order_by(desc(func.count(Feed.post_id)))
       .limit(limit)
       .all()
   )


   return results



