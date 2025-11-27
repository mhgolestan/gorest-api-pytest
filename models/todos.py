from typing import TypedDict

from pydantic import BaseModel, Field, RootModel

from models.base import BaseResource, BaseResourceDict
from utils.fakers import random_todo_status, random_string, random_due_date


class UpdateTodo(BaseModel):
    title: str | None = Field(default_factory=random_string)
    due_on: str | None = Field(default_factory=random_due_date)
    status: str | None = Field(default_factory=random_todo_status)


class DefaultTodo(BaseResource):
    due_on: str = Field(default_factory=random_due_date)
    status: str = Field(default_factory=random_todo_status)


class DefaultTodosList(RootModel):
    root: list[DefaultTodo]


class TodoDict(BaseResourceDict, TypedDict):
    due_on: str
    status: str