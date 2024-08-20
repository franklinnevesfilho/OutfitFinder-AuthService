from typing import Optional

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import subqueryload

from app.config import database
from app.models import User, RefreshToken
from app.schemas import UserLogin, LoginResponse, Response
from app.handlers import jwt

async def get_token(userLogin: UserLogin) -> Response:
    session = database.get_session()

    try:
        user: Optional[User] = session.query(User).filter_by(email=userLogin.email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        access_token = jwt.sign_jwt(
            {
                "sub": user.id,
                "roles": [role.name for role in user.roles]
            }
        )
        return Response(node={"access_token": access_token}, status=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def login(userLogin: UserLogin) -> Response:
    session = database.get_session()
    try:
        user: Optional[User] = (session.query(User).options(subqueryload(User.roles)).filter_by(email=userLogin.email).first())
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not user.verify_password(userLogin.password):
            raise HTTPException(status_code=401, detail="Invalid password")

        refresh_token = RefreshToken(
            token=str(jwt.generate_refresh_token()),
            user_id=user.id
        )

        session.add(refresh_token)
        session.commit()


        login_response = LoginResponse(
            access_token=jwt.sign_jwt(
                {
                    "sub": user.id,
                    "rls": [role.name for role in user.roles]
                 }),
            refresh_token=refresh_token.token
        )
        return Response(node=login_response.model_dump(), status=200)

    except SQLAlchemyError:
        session.rollback()
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        session.close()

async def logout(jwtToken: str) -> Response:
    session = database.get_session()
    try:
        decoded_token = jwt.decode_jwt(jwtToken)
        user_id = decoded_token["sub"]
        session.query(RefreshToken).filter_by(user_id=user_id).delete()
        session.commit()
        return Response(node={"message": "Logout successful"}, status=200)
    except SQLAlchemyError:
        session.rollback()
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()
    
