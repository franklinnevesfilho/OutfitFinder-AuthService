from pydantic import BaseModel, Field

"""
User Schema Module

This module contains all the schemas for the User object within the service.

Classes:
    User: The User schema used to return all attributes.
    UserLogin: The UserLogin, used for authentication.
    UserRegistration: The UserRegistration, used for registration.   
"""

class User(BaseModel):
    firstname: str = Field(..., examples=["John"])
    lastname: str = Field(..., examples=["Doe"])
    email: str = Field(..., examples=["johndoe@mail.com"])
    roles: list[str] = Field(..., examples=[["user"]])
    two_factor_enabled: bool = Field(..., examples=[False])
    profile_picture: str = Field(..., examples=["profile_picture.jpg"])

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "firstname": "John",
                "lastname": "Doe",
                "email": "johndoe@mail.com",
                "roles": ["user"],
                "two_factor_enabled": False,
                "profile_picture": "johndoe_profilePic_123456.jpg"
            }
        }

class UserLogin(BaseModel):
    email: str = Field(..., examples=["johndoe@mail.com"])
    password: str = Field(..., examples=["password"])

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "email": "johndoe@mail.com",
                "password": "password",
            }
        }

class UserRegistration(BaseModel):
    firstname: str = Field(..., examples=["John"])
    lastname: str = Field(..., examples=["Doe"])
    email: str = Field(..., examples=["johndoe@mail.com"])
    password: str = Field(..., examples=["password"])

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "firstname": "John",
                "lastname": "Doe",
                "email": "johndoe@mail.com",
                "password": "password"
            }
        }
