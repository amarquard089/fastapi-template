"""Base class for User entity, containing common attributes and validation logic."""

from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    """Base class for User entity, containing common attributes and validation logic."""

    first_name: str = Field(max_length=50, min_length=1)
    last_name: str = Field(max_length=50, min_length=1)
    email: str = Field(max_length=255, min_length=1)
