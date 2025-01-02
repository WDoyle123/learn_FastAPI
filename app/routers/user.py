from typing import List

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Response
from sqlalchemy.orm import Session

from .. import models, schemas, utils
from ..db import engine, get_db

router = APIRouter(
    prefix="/users"
)


@router.get("/", status_code=200, response_model=List[schemas.UserOut])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.post("/", status_code=201, response_model=schemas.UserOut)
async def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with id: {id} does not exist"
        )

    return user
