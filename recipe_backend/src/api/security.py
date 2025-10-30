from datetime import datetime, timedelta, timezone
from typing import Optional
import hashlib
import hmac
import base64
import json

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .config import get_settings, get_access_token_expires_delta
from .db import get_db
from .models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
settings = get_settings()


def _hash_password(password: str, salt: str) -> str:
    """Return salted SHA256 hash. Simple dev-friendly hasher. Replace with passlib in production."""
    h = hashlib.sha256()
    h.update((salt + password).encode("utf-8"))
    return h.hexdigest()


# PUBLIC_INTERFACE
def hash_password(password: str, email_as_salt: str) -> str:
    """Hash password using email as salt for demo purposes."""
    return _hash_password(password, email_as_salt.lower())


# Minimal JWT (HS256) without external libs to avoid extra deps.
def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(data: str) -> bytes:
    pad = '=' * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + pad)


# PUBLIC_INTERFACE
def create_access_token(user: User, expires_delta: Optional[timedelta] = None) -> str:
    """Create a signed JWT for a user."""
    if expires_delta is None:
        expires_delta = get_access_token_expires_delta()
    now = datetime.now(tz=timezone.utc)
    exp = now + expires_delta
    header = {"alg": settings.JWT_ALG, "typ": "JWT"}
    payload = {
        "sub": str(user.id),
        "email": user.email,
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
    }
    signing_input = ".".join([_b64url(json.dumps(header, separators=(',', ':')).encode()),
                              _b64url(json.dumps(payload, separators=(',', ':')).encode())])
    signature = hmac.new(settings.JWT_SECRET.encode(), signing_input.encode(), hashlib.sha256).digest()
    token = signing_input + "." + _b64url(signature)
    return token


# PUBLIC_INTERFACE
def verify_token(token: str) -> dict:
    """Verify token signature and expiry and return payload dict."""
    try:
        header_b64, payload_b64, signature_b64 = token.split(".")
        signing_input = header_b64 + "." + payload_b64
        expected_sig = hmac.new(settings.JWT_SECRET.encode(), signing_input.encode(), hashlib.sha256).digest()
        if not hmac.compare_digest(expected_sig, _b64url_decode(signature_b64)):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token signature")
        payload = json.loads(_b64url_decode(payload_b64))
        if int(payload.get("exp", 0)) < int(datetime.now(tz=timezone.utc).timestamp()):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
        return payload
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


# PUBLIC_INTERFACE
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    """FastAPI dependency that extracts and returns the current user from JWT."""
    payload = verify_token(token)
    user_id = int(payload.get("sub"))
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
