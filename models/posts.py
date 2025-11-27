from typing import TypedDict

from pydantic import BaseModel, Field, RootModel

from utils.fakers import random_number, random_string, random_email, random_gender, random_status


class UpdatePost(BaseModel):
    title: str | None = Field(default_factory=random_string)
    body: str | None = Field(default_factory=random_string)


class DefaultPost(BaseModel):
    id: int = Field(default_factory=random_number)
    user_id: int = Field(default_factory=random_number)
    title: str = Field(default_factory=random_string)
    body: str = Field(default_factory=random_string)


class DefaultPostsList(RootModel):
    root: list[DefaultPost]


class PostDict(TypedDict):
    id: int
    user_id: int
    title: str
    body: str