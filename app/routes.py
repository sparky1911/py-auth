from fastapi import APIRouter,Depends,HTTPException
from app.database import get_db
from app.models import User
from app.schemas import UserCreate,UserLogin,RefreshRequest
from sqlalchemy.orm import Session
from app.models import RefreshToken
from datetime import datetime,timedelta,timezone,UTC
from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    hash_refresh_token,
    REFRESH_TOKEN_EXPIRE_DAYS,
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
    access_token = create_access_token(
        {"sub": str(db_user.id)}
    )
    refresh_token=create_refresh_token()
    db_refresh_token=RefreshToken(
        user_id=db_user.id,
        token_hash=hash_refresh_token(refresh_token),
        expires_at=datetime.now(timezone.utc)+timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    )
    db.add(db_refresh_token)
    db_user.last_login_at=datetime.now(timezone.utc)
    db.commit()
    db.refresh(db_refresh_token)
    return {
    "access_token": access_token,
    "refresh_token": refresh_token,
    "token_type": "bearer"
    }


@router.post("/refresh")
def refresh_token(
    payload: RefreshRequest,
    db: Session = Depends(get_db)
):
    token_hash = hash_refresh_token(
        payload.refresh_token
    )

    db_token = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.token_hash == token_hash
        )
        .first()
    )

    if not db_token:
        raise HTTPException(
            status_code=401,
            detail="invalid token"
        )

    if db_token.revoked:
        raise HTTPException(
            status_code=401,
            detail="refresh token revoked"
        )

    if db_token.expires_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=401,
            detail="refresh token expired"
        )
    db_token.revoked=True
    new_refresh_token=create_refresh_token()
    new_db_token=RefreshToken(
        user_id=db_token.user_id,
        token_hash=hash_refresh_token(new_refresh_token),
        expires_at=datetime.now(timezone.utc)
                + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
            )
    db.add(new_db_token)
    access_token = create_access_token(
        {"sub": str(db_token.user_id)}
    )
    db.commit()

    return {
    "access_token": access_token,
    "refresh_token": new_refresh_token,
    "token_type": "bearer",
    }
    
@router.post("/logout")
def logout(payload:RefreshRequest, db :Session = Depends(get_db)):
    token_hash=hash_refresh_token(payload.refresh_token)
    db_token = ( db.query(RefreshToken).filter(RefreshToken.token_hash==token_hash).first())
    if not db_token:
        raise HTTPException(status_code=401,detail="invalid refresh token")
    db_token.revoked=True
    db.commit()
    return{
        "message":"logged out successfully"
    }