from typing import Optional
from sqlalchemy.orm import Session

from ..models import User
from ..repositories import (
    get_user_by_email,
    create_user as repo_create_user,
    authenticate_user as repo_authenticate_user,
)
from ..security import create_access_token


# PUBLIC_INTERFACE
def register_user(db: Session, email: str, password: str, full_name: Optional[str] = None) -> str:
    """Register a new user and return a JWT access token."""
    existing = get_user_by_email(db, email)
    if existing:
        raise ValueError("Email already registered")
    user: User = repo_create_user(db, email=email, password=password, full_name=full_name)
    token = create_access_token(user)
    return token


# PUBLIC_INTERFACE
def login_user(db: Session, email: str, password: str) -> Optional[str]:
    """Authenticate user credentials and return a JWT access token on success."""
    user = repo_authenticate_user(db, email, password)
    if not user:
        return None
    token = create_access_token(user)
    return token
