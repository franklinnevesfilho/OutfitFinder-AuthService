from datetime import datetime, timedelta
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    token = Column(String(100), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id"))
    user = relationship("User", back_populates="refresh_tokens")
    created_at = Column(DateTime, default=datetime.now())
    expires = Column(DateTime, default=lambda: datetime.now() + timedelta(days=7))
