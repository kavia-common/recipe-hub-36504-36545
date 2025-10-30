from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .db import get_db
from .schemas import UserOut, UserUpdate
from .security import get_current_user
from .models import User
from .repositories import list_users as repo_list_users, update_user as repo_update_user, delete_user as repo_delete_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserOut, summary="Get current user", description="Return the profile of the authenticated user.")
def get_me(current_user: User = Depends(get_current_user)) -> User:
    return current_user


@router.patch("/me", response_model=UserOut, summary="Update current user", description="Update the profile or password of the authenticated user.")
def update_me(payload: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> User:
    updated = repo_update_user(db, current_user, full_name=payload.full_name, password=payload.password)
    return updated


@router.delete("/me", status_code=204, summary="Delete account", description="Delete the authenticated user's account.")
def delete_me(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo_delete_user(db, current_user)
    return None


@router.get("/", response_model=List[UserOut], summary="List users", description="List all users. For demo only; not access-restricted.")
def list_users(db: Session = Depends(get_db)) -> list[User]:
    return repo_list_users(db)
