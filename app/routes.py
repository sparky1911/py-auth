from fastapi import APIRouter,Depends,HTTPException
from app.database import get_db
from app.models import User
from app.schemas import UserCreate,UserLogin
from sqlalchemy.orm import Session
from app.auth import (
    hash_password,
    verify_password,
    create_access_token
)



router=APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "healthy-v2"
    }


@router.post("/signup")
def signup(user:UserCreate, db: Session=Depends(get_db)):
    existing_user=db.query(User).filter(
        User.email==user.email
    ).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="user alread exists")
    new_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hash_password(
            user.password
        )
    )
    db.add(new_user)
    db.commit()
    return {
        "message":"user_created"
    }



@router.post("/login")
def login(user:UserLogin ,db: Session=Depends(get_db)):
    db_user=db.query(User).filter(
        User.email==user.email
    ).first()
    if not db_user:
        raise HTTPException(status_code=401,detail="Invalid credentials")
    if not verify_password(user.password,db_user.hashed_password):
        raise HTTPException(status_code=401,detail="Invalid Credentials")
    token = create_access_token(
        {"sub": str(db_user.id)}
    )
    return {
        "access_token": token
    }
