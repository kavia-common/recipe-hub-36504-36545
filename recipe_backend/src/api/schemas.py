from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

# AUTH

class Token(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")


class TokenData(BaseModel):
    user_id: int = Field(..., description="User identifier encoded in token")
    email: EmailStr = Field(..., description="User email")


# USER

class UserBase(BaseModel):
    email: EmailStr = Field(..., description="Unique email for the user")
    full_name: Optional[str] = Field(None, description="Full name")


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="Password for the account")


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, description="Full name")
    password: Optional[str] = Field(None, min_length=6, description="New password")


class UserOut(UserBase):
    id: int = Field(..., description="User ID")
    created_at: datetime

    class Config:
        from_attributes = True


# RECIPE

class RecipeBase(BaseModel):
    title: str = Field(..., description="Recipe title")
    description: Optional[str] = Field(None, description="Short description")
    ingredients: Optional[str] = Field(None, description="Ingredients list (free-form text)")
    instructions: Optional[str] = Field(None, description="Cooking instructions")


class RecipeCreate(RecipeBase):
    pass


class RecipeUpdate(BaseModel):
    title: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    ingredients: Optional[str] = Field(None)
    instructions: Optional[str] = Field(None)


class RecipeOut(RecipeBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
