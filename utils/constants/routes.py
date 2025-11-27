from enum import Enum


class APIRoutes(str, Enum):
    USERS = '/users'
    POSTS = '/posts'
    COMMENTS = '/comments'
    TODOS = '/todos'

    def __str__(self) -> str:
        return self.value