from .base import Base
from ..config import PasswordUtil
from sqlalchemy import Column, String, Table, ForeignKey
from sqlalchemy.orm import relationship
import uuid

user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', String(36), ForeignKey('users.id')),
    Column('role_id', String(36), ForeignKey('roles.id'))
)


class User(Base):
    __tablename__ = 'users'
    id = Column(String(36), default=lambda: str(uuid.uuid4()), primary_key=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    _password = Column(String(100))

    roles = relationship("Role", secondary=user_roles, back_populates="users")

    # New relationship with RefreshToken
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")

    @property
    def full_name(self):
        return f'{self.firstname} {self.lastname}'

    def set_password(self, password):
        self._password = PasswordUtil.hash_password(password)

    def verify_password(self, password: str):
        return PasswordUtil.check_password(password, self._password)
