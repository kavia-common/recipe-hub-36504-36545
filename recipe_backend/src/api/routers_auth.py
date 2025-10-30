from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .db import get_db
from .schemas import Token
from .repositories import authenticate_user, create_user, get_user_by_email
from .security import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=Token, summary="Register user", description="Create a new user and return an access token.")
def register(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm has username and password; use username as email
    existing = get_user_by_email(db, form.username)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = create_user(db, email=form.username, password=form.password, full_name=None)
    token = create_access_token(user)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/token", response_model=Token, summary="Login", description="Obtain an access token via username(email) and password.")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    token = create_access_token(user)
    return {"access_token": token, "token_type": "bearer"}
