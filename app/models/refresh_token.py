from datetime import datetime,timezone

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.database import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"),nullable=False,)
    token_hash = Column(String(255),unique=True,nullable=False,)
    expires_at = Column(DateTime(timezone=True),nullable=False,)
    created_at = Column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc),nullable=False,)
    revoked = Column(Boolean,default=False,nullable=False,)
    user = relationship("User",back_populates="refresh_tokens",)