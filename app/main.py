import os
from random import randrange
from typing import Optional

import psycopg
from fastapi import FastAPI, HTTPException, Response
from fastapi.params import Body
from psycopg.rows import dict_row
from pydantic import BaseModel


def load_secrets_from_file(file_path):
    with open(file_path) as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                os.environ[key] = value


load_secrets_from_file(".secrets.sh")

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


while True:
    try:
        conn = psycopg.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )
        cursor = conn.cursor(row_factory=dict_row)
        print("Database Connection was Successful")
        break
    except Exception as e:
        print(f"Connection to DB failed: {e}")
        time.sleep(2)


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=201)
async def create_posts(post: Post):
    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
        (post.title, post.content, post.published),
    )
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/{id}", status_code=201)
async def get_post(id: int):
    cursor.execute(
        """SELECT * FROM posts WHERE id = %s""",
        (id,),
    )
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=404, detail=f"post with id: {id} was not found")
    return {"data": post}


@app.delete("/posts/{id}", status_code=204)
async def delete_post(id: int):
    cursor.execute(
        """DELETE FROM posts WHERE id = %s RETURNING *""",
        (str(id),),
    )
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=404, detail=f"post with id: {id} was not found")
    conn.commit()


@app.put("/posts/{id}", status_code=201)
async def update_post(id: int, post: Post):
    cursor.execute(
        """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
        (post.title, post.content, post.published, str(id)),
    )
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=404, detail=f"post with id: {id} was not found")
    conn.commit()
    return {"data": post}
