from sqlalchemy import create_engine
from app.models import Role, User
import os

# Database configuration
_DatabaseConfig = {
    "NAME": os.getenv("DB_NAME", "auth_db"),
    "USER": os.getenv("DB_USER", "user"),
    "PASSWORD": os.getenv("DB_PASSWORD", "password"),
    "HOST": os.getenv("DB_HOST", "localhost"),
    "PORT": os.getenv("DB_PORT", "3308"),
    "TYPE": os.getenv("DB_TYPE", "mysql")
}

_engine = None


def _get_database_uri() -> str:
    db_type = _DatabaseConfig.get('TYPE')

    if db_type == 'sqlite':
        return f'sqlite:///{_DatabaseConfig.get("NAME")}.db'
    elif db_type == 'mysql':
        return f'mysql+pymysql://{_DatabaseConfig.get("USER")}:{_DatabaseConfig.get("PASSWORD")}@{_DatabaseConfig.get("HOST")}:{_DatabaseConfig.get("PORT")}/{_DatabaseConfig.get("NAME")}'
    else:
        raise Exception('Database type not supported')

def get_engine():
    global _engine
    if not _engine:
        _engine = create_engine(_get_database_uri())
    return _engine

def get_session():
    from sqlalchemy.orm import sessionmaker
    session = sessionmaker(bind=get_engine())
    return session()

def db_shutdown():
    from app.models import Base
    Base.metadata.drop_all(bind=get_engine())

def db_init():
    session = get_session()

    roles = ['admin', 'user']
    existing_roles = session.query(Role).all()

    if existing_roles:
        session.close()
        return
    else:
        for role in roles:
            session.add(Role(name=role))

        session.commit()

    admin = User(
        firstname='admin',
        lastname='admin',
        email='admin@admin.com'
    )
    admin.set_password('admin')

    base_user = User(
        firstname='user',
        lastname='user',
        email="user@mail.com"
    )
    base_user.set_password('password')

    session.add(admin)
    session.add(base_user)


    user_role = session.query(Role).filter_by(name='user').first()
    admin_role = session.query(Role).filter_by(name='admin').first()

    admin.roles.append(admin_role)
    base_user.roles.append(user_role)

    session.commit()
    session.close()