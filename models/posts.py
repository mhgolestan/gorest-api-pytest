from typing import TypedDict

from pydantic import BaseModel, Field, RootModel

from models.base import BaseResource, BaseResourceDict
from utils.fakers import random_string


class UpdatePost(BaseModel):
    title: str | None = Field(default_factory=random_string)
    body: str | None = Field(default_factory=random_string)


class DefaultPost(BaseResource):
    body: str = Field(default_factory=random_string)


class DefaultPostsList(RootModel):
    root: list[DefaultPost]


class PostDict(BaseResourceDict, TypedDict):
    body: str