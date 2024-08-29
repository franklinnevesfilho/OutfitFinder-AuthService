from .base import Base
from app.utils import PasswordUtil
from sqlalchemy import Column, String, Table, ForeignKey, Boolean
from sqlalchemy.orm import relationship
import uuid

user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', String(36), ForeignKey('users.id')),
    Column('role_id', String(36), ForeignKey('roles.id'))
)


class User(Base):
    """
    User model

    Attributes:
    -----------
    id : str
        The user's unique identifier
    firstname : str
        The user's first name
    lastname : str
        The user's last name
    email : str
        The user's email address
    phone_number : str
        The user's phone number
    _password : str
        The user's hashed password
    two_factor_enabled : bool
        Whether the user has two-factor authentication enabled
    profile_picture : str
        The user's profile picture URL
    roles : List[Role]
        The roles assigned to the user

    full_name : str
        The user's full name (read-only)

    Methods:
    --------
    set_password(password: str) -> None
        Set the user's password
    verify_password(password: str) -> bool
        Verify the user's password
    """
    __tablename__ = 'users'
    id = Column(String(36), default=lambda: str(uuid.uuid4()), primary_key=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    phone_number = Column(String(50), nullable=True, default=None)
    _password = Column(String(100))
    verified = Column(Boolean, default=False)
    two_factor_enabled = Column(Boolean, default=False)
    profile_picture = Column(String(100), default=None)

    roles = relationship("Role", secondary=user_roles, back_populates="users")

    @property
    def full_name(self):
        return f'{self.firstname} {self.lastname}'

    def set_password(self, password):
        self._password = PasswordUtil.hash_password(password)

    def verify_password(self, password: str):
        return PasswordUtil.check_password(password, self._password)
