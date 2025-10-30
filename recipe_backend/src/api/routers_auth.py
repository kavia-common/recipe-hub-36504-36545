from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .db import get_db
from .schemas import Token
from .services.auth_service import register_user, login_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=Token, summary="Register user", description="Create a new user and return an access token.")
def register(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm has username and password; use username as email
    try:
        token = register_user(db, email=form.username, password=form.password, full_name=None)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return {"access_token": token, "token_type": "bearer"}


@router.post("/token", response_model=Token, summary="Login", description="Obtain an access token via username(email) and password.")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    token = login_user(db, email=form_data.username, password=form_data.password)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    return {"access_token": token, "token_type": "bearer"}
