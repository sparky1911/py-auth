from sqlalchemy import Column,Integer,String,Boolean,DateTime
from app.database import Base
from datetime import datetime,timezone
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True,index=True)
    email=Column(String(255),unique=True,nullable=False)
    username=Column(String(32),unique=True,nullable=False)
    first_name=Column(String(100),nullable=True)
    last_name=Column(String(100),nullable=True)
    hashed_password=Column(String(255),nullable=False)
    is_active=Column(Boolean,default=True,nullable=False)
    is_verified=Column(Boolean,default=False,nullable=False)
    created_at=Column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc),nullable=False)
    updated_at=Column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc),nullable=False)
    last_login_at=Column(DateTime(timezone=True),nullable=True)
    refresh_tokens=relationship("RefreshToken",back_populates="user",cascade="all, delete-orphan",)
