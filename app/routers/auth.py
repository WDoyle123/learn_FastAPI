from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import db, models, schemas, utils

router = APIRouter(tags=["Authentication"])


@router.post("/login", status_code=201)
def login(user_credentials: schemas.UserLogin, db: Session = Depends(db.get_db)):
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.email)
        .first()
    )

    if not user:
        raise HTTPException(status_code=404, detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=404, detail=f"Invalid Credentials")

    # create token
    # return token

    return {"token": "example token"}
