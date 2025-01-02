import os

from fastapi import FastAPI

from . import models, schemas
from .db import engine, get_db
from .routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def load_secrets_from_file(file_path):
    with open(file_path) as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                os.environ[key] = value


load_secrets_from_file(".secrets.sh")

app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
