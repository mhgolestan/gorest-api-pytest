"""
Mock API responses for CI environments where the real API is blocked by Cloudflare.
"""
import json
import re
import httpx
import respx
from settings import base_settings


# Track deleted user IDs for proper 404 responses after deletion
_deleted_user_ids: set[str] = set()


def reset_deleted_users() -> None:
    """Reset the deleted users tracking set."""
    global _deleted_user_ids
    _deleted_user_ids = set()


def setup_api_mocks(respx_mock: respx.MockRouter) -> None:
    """Configure all API mock routes."""
    base_url = base_settings.api_url
    
    # === POSTS ROUTES (more specific, must come first) ===
    _setup_posts_mocks(respx_mock, base_url)
    
    # === TODOS ROUTES (more specific, must come first) ===
    _setup_todos_mocks(respx_mock, base_url)
    
    # === USERS ROUTES (less specific, must come last) ===
    _setup_users_mocks(respx_mock, base_url)


def _setup_posts_mocks(respx_mock: respx.MockRouter, base_url: str) -> None:
    """Setup mock routes for posts endpoints."""
    # Mock GET /posts
    respx_mock.get(f"{base_url}posts").mock(return_value=httpx.Response(
        200,
        json=[
            {"id": 1, "user_id": 1, "title": "Test Post", "body": "Test body content"},
            {"id": 2, "user_id": 1, "title": "Another Post", "body": "More content"},
        ]
    ))
    
    # Mock GET /users/{id}/posts - MUST come before /users/{id}
    respx_mock.get(url__regex=rf"{base_url}users/\d+/posts$").mock(return_value=httpx.Response(
        200,
        json=[{"id": 1, "user_id": 1, "title": "Test Post", "body": "Test body content"}]
    ))
    
    # Mock POST /users/{id}/posts
    respx_mock.post(url__regex=rf"{base_url}users/\d+/posts$").mock(side_effect=_mock_create_post)


def _setup_todos_mocks(respx_mock: respx.MockRouter, base_url: str) -> None:
    """Setup mock routes for todos endpoints."""
    # Mock GET /todos
    respx_mock.get(f"{base_url}todos").mock(return_value=httpx.Response(
        200,
        json=[
            {"id": 1, "user_id": 1, "title": "Test Todo", "due_on": "2024-12-31T23:59:59.000+05:30", "status": "pending"},
        ]
    ))
    
    # Mock GET /users/{id}/todos - MUST come before /users/{id}
    respx_mock.get(url__regex=rf"{base_url}users/\d+/todos$").mock(return_value=httpx.Response(
        200,
        json=[{"id": 1, "user_id": 1, "title": "Test Todo", "due_on": "2024-12-31T23:59:59.000+05:30", "status": "pending"}]
    ))
    
    # Mock POST /users/{id}/todos
    respx_mock.post(url__regex=rf"{base_url}users/\d+/todos$").mock(side_effect=_mock_create_todo)
    
    # Mock DELETE /users/{id}/todos/{id}
    respx_mock.delete(url__regex=rf"{base_url}users/\d+/todos/\d+$").mock(return_value=httpx.Response(204))


def _setup_users_mocks(respx_mock: respx.MockRouter, base_url: str) -> None:
    """Setup mock routes for users endpoints."""
    # Mock GET /users
    respx_mock.get(f"{base_url}users").mock(return_value=httpx.Response(
        200,
        json=[
            {"id": 1, "name": "Test User", "email": "test@example.com", "gender": "male", "status": "active"},
            {"id": 2, "name": "Jane Doe", "email": "jane@example.com", "gender": "female", "status": "active"},
        ]
    ))
    
    # Mock GET /users/{id} - handle all cases including SQL injection attempts
    respx_mock.get(url__regex=rf"{base_url}users/[^/]+$").mock(side_effect=_mock_get_user)
    
    # Mock POST /users - success
    respx_mock.post(f"{base_url}users").mock(side_effect=_mock_create_user)
    
    # Mock PATCH /users/{id} - handle all cases
    respx_mock.patch(url__regex=rf"{base_url}users/[^/]+$").mock(side_effect=_mock_update_user)
    
    # Mock DELETE /users/{id} - handle all cases
    respx_mock.delete(url__regex=rf"{base_url}users/[^/]+$").mock(side_effect=_mock_delete_user)


# === Helper Functions ===

def _extract_user_id(url: str) -> str:
    """Extract user ID from URL."""
    match = re.search(r'/users/([^/]+)$', str(url))
    return match.group(1) if match else ""


def _is_valid_user_id(user_id: str) -> bool:
    """Check if user ID is a valid positive integer."""
    try:
        id_int = int(user_id)
        return id_int > 0 and id_int != 999999  # 999999 is treated as "not found"
    except ValueError:
        return False


# === Mock Response Handlers ===

def _mock_get_user(request: httpx.Request) -> httpx.Response:
    """Mock GET /users/{id} with proper handling."""
    user_id = _extract_user_id(str(request.url))
    
    # Check if user was deleted
    if user_id in _deleted_user_ids:
        return httpx.Response(404, json={"message": "Resource not found"})
    
    # Invalid user IDs (non-numeric, SQL injection attempts, special values)
    if not _is_valid_user_id(user_id):
        return httpx.Response(404, json={"message": "Resource not found"})
    
    # Valid user ID
    return httpx.Response(200, json={
        "id": int(user_id),
        "name": "Test User",
        "email": "test@example.com",
        "gender": "male",
        "status": "active"
    })


def _mock_create_user(request: httpx.Request) -> httpx.Response:
    """Mock user creation with validation."""
    try:
        data = json.loads(request.content)
    except (json.JSONDecodeError, TypeError):
        data = {}
    
    # Validate required fields
    if not data.get('name') or not data.get('email') or not data.get('gender') or not data.get('status'):
        return httpx.Response(422, json=[{"field": "name", "message": "can't be blank"}])
    
    # Validate email format
    if '@' not in str(data.get('email', '')):
        return httpx.Response(422, json=[{"field": "email", "message": "is invalid"}])
    
    # Check for overflow (name or email too long)
    if len(str(data.get('name', ''))) > 1000 or len(str(data.get('email', ''))) > 1000:
        return httpx.Response(422, json=[{"field": "name", "message": "is too long"}])
    
    return httpx.Response(201, json={
        "id": 12345,
        "name": data.get('name'),
        "email": data.get('email'),
        "gender": data.get('gender'),
        "status": data.get('status')
    })


def _mock_update_user(request: httpx.Request) -> httpx.Response:
    """Mock user update with proper handling."""
    user_id = _extract_user_id(str(request.url))
    
    # Check if user was deleted
    if user_id in _deleted_user_ids:
        return httpx.Response(404, json={"message": "Resource not found"})
    
    # Invalid user IDs
    if not _is_valid_user_id(user_id):
        return httpx.Response(404, json={"message": "Resource not found"})
    
    try:
        data = json.loads(request.content)
    except (json.JSONDecodeError, TypeError):
        data = {}
    
    # Check for overflow
    if len(str(data.get('name', ''))) > 1000:
        return httpx.Response(422, json=[{"field": "name", "message": "is too long"}])
    
    return httpx.Response(200, json={
        "id": int(user_id),
        "name": data.get('name', 'Updated User'),
        "email": data.get('email', 'updated@example.com'),
        "gender": data.get('gender', 'male'),
        "status": data.get('status', 'active')
    })


def _mock_delete_user(request: httpx.Request) -> httpx.Response:
    """Mock user deletion with proper handling."""
    global _deleted_user_ids
    user_id = _extract_user_id(str(request.url))
    
    # Check if already deleted
    if user_id in _deleted_user_ids:
        return httpx.Response(404, json={"message": "Resource not found"})
    
    # Invalid user IDs
    if not _is_valid_user_id(user_id):
        return httpx.Response(404, json={"message": "Resource not found"})
    
    # Mark as deleted
    _deleted_user_ids.add(user_id)
    return httpx.Response(204)


def _mock_create_post(request: httpx.Request) -> httpx.Response:
    """Mock post creation with validation."""
    try:
        data = json.loads(request.content)
    except (json.JSONDecodeError, TypeError):
        data = {}
    
    # Validate required fields
    if not data.get('title') or not data.get('body'):
        return httpx.Response(422, json=[{"field": "title", "message": "can't be blank"}])
    
    return httpx.Response(201, json={
        "id": 12345,
        "user_id": 1,
        "title": data.get('title'),
        "body": data.get('body')
    })


def _mock_create_todo(request: httpx.Request) -> httpx.Response:
    """Mock todo creation with validation."""
    try:
        data = json.loads(request.content)
    except (json.JSONDecodeError, TypeError):
        data = {}
    
    # Validate required fields - need title, due_on, and status
    if not data.get('title') or not data.get('due_on') or not data.get('status'):
        return httpx.Response(422, json=[{"field": "title", "message": "can't be blank"}])
    
    return httpx.Response(201, json={
        "id": 12345,
        "user_id": 1,
        "title": data.get('title'),
        "due_on": data.get('due_on'),
        "status": data.get('status')
    })
