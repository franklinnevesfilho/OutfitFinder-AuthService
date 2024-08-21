from .base import Base
import uuid
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Role(Base):
    """
    Role model

    Attributes:
    -----------
    id : str
        The role's unique identifier
    name : str
        The role's name

    users : List[User]
        The users assigned to the role
    """
    __tablename__ = 'roles'
    id = Column(String(36), default=lambda: str(uuid.uuid4()), primary_key=True)
    name = Column(String(50), nullable=False)

    users = relationship("User", secondary='user_roles', back_populates="roles")