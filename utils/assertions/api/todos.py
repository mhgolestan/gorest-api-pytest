from models.todos import DefaultTodo, TodoDict, UpdateTodo
from utils.assertions.base.expect import expect


def assert_todo(
    expected_todo: TodoDict,
    actual_todo: DefaultTodo | UpdateTodo
):
    if isinstance(actual_todo, DefaultTodo):
        expect(expected_todo['id']) \
            .set_description('Todo "id"')\
            .to_be_equal(actual_todo.id)

    expect(expected_todo['user_id']) \
        .set_description('Todo "user_id"') \
        .to_be_equal(actual_todo.user_id)

    expect(expected_todo['title']) \
        .set_description('Todo "title"') \
        .to_be_equal(actual_todo.title)
    
    expect(expected_todo['due_on']) \
        .set_description('Todo "due_on"') \
        .to_be_equal(actual_todo.due_on)

    expect(expected_todo['status']) \
        .set_description('Todo "status"') \
        .to_be_equal(actual_todo.status)