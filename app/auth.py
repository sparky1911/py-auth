import os
from dotenv import load_dotenv
from passlib.context import CryptContext
from datetime import datetime, timedelta,timezone,UTC
from jose import jwt
import secrets
import hashlib
import secrets



load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 30
SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

def hash_password(password:str):
    return pwd_context.hash(password)


def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data:dict):
    to_encode=data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=30
    )
    to_encode.update({"exp":expire,"type":"access"})
    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def create_refresh_token():
    return secrets.token_urlsafe(64)

def hash_refresh_token(token: str):
    return hashlib.sha256(
        token.encode()
    ).hexdigest()
