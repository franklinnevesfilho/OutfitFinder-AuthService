from pydantic import BaseModel, Field

"""
Schema for User Login
"""
class UserLogin(BaseModel):
    email: str = Field(..., examples=["ueser@mail.com"])
    password: str = Field(..., examples=["password"])

    class Config:
        from_attributes = True
