from datetime import datetime, timedelta
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class SessionToken(Base):
    """
    Session token model

    Attributes:
    -----------
    token : str
        The refresh token
    user_id : str
        The user's unique identifier
    user : User
        The user associated with the refresh token
    created_at : datetime
        The date and time the refresh token was created
    expires : datetime
        The date and time the refresh token expires

    Methods:
    --------
    has_expired() -> bool
        Check if the refresh token has expired
    """
    __tablename__ = "session_tokens"

    token = Column(String(100), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id"))
    user = relationship("User", back_populates="refresh_tokens")
    created_at = Column(DateTime, default=datetime.now())
