from typing import TypedDict

from pydantic import BaseModel, Field, RootModel

from utils.fakers import random_number, random_string


class BaseResource(BaseModel):
    id: int = Field(default_factory=random_number)
    user_id: int = Field(default_factory=random_number)
    title: str = Field(default_factory=random_string)


class BaseResourceDict(TypedDict):
    id: int
    user_id: int
    title: str