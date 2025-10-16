#!/usr/bin/python3
"""Authentication helpers: password hashing and JWT tokens."""
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from os import getenv


# Secret configuration - for production keep this in env vars / secrets manager
SECRET_KEY = getenv("SECRET_KEY", None)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    now = datetime.utcnow()
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "iat": now})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(lambda: None)):
    # This is a placeholder for FastAPI's OAuth2 dependency wiring in routes.
    # Real dependency will use OAuth2PasswordBearer to extract the token.
    raise NotImplementedError("Use OAuth2 dependency in routes to wire this")


def require_role(required_role: str):
    def _dependency(current_user: dict = Depends(get_current_user)):
        if not current_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Not authenticated")
        if current_user.get("role") != required_role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Insufficient permissions")
        return current_user
    return _dependency
