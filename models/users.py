from typing import TypedDict

from pydantic import BaseModel, Field, RootModel

from utils.fakers import random_number, random_string, random_email, random_gender, random_status


class UpdateUser(BaseModel):
    name: str | None = Field(default_factory=random_string)
    email: str | None = Field(default_factory=random_email)
    gender: str | None = Field(default_factory=random_gender)
    status: str | None = Field(default_factory=random_status)


class DefaultUser(BaseModel):
    id: int = Field(default_factory=random_number)
    name: str = Field(default_factory=random_string)
    email: str = Field(default_factory=random_email)
    gender: str = Field(default_factory=random_gender)
    status: str = Field(default_factory=random_status)


class DefaultUsersList(RootModel):
    root: list[DefaultUser]


class UserDict(TypedDict):
    id: int
    name: str
    email: str
    gender: str
    status: str