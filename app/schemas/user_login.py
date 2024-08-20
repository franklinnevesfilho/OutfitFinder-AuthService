from pydantic import BaseModel, Field

class UserLogin(BaseModel):
    email: str = Field(..., examples=["admin@admin.com"])
    password: str = Field(..., examples=["admin"])

    class Config:
        from_attributes = True
