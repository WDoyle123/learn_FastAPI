import os
from random import randrange
from typing import List, Optional

import psycopg
from fastapi import Depends, FastAPI, HTTPException, Response
from fastapi.params import Body
from psycopg.rows import dict_row
from sqlalchemy.orm import Session

from . import models, schemas, utils
from .db import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def load_secrets_from_file(file_path):
    with open(file_path) as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                os.environ[key] = value


load_secrets_from_file(".secrets.sh")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts", response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=201, response_model=schemas.Post)
async def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}", status_code=201, response_model=schemas.Post)
async def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail=f"post with id: {id} was not found")
    return post


@app.delete("/posts/{id}", status_code=204)
async def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail=f"post with id: {id} was not found")
    db.delete(post)
    db.commit()
    return Response(status_code=204)


@app.put("/posts/{id}", status_code=201, response_model=schemas.Post)
async def update_post(
    id: int, update_post: schemas.PostCreate, db: Session = Depends(get_db)
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=404, detail=f"post with id: {id} was not found")
    post_query.update(update_post.dict())
    db.commit()
    return post_query.first()


@app.get("/users", status_code=200, response_model=List[schemas.UserOut])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@app.post("/users", status_code=201, response_model=schemas.UserOut)
async def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with id: {id} does not exist"
        )

    return user
