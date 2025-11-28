import os
import pytest
import httpx
import respx
from settings import base_settings
from utils.mocks.api_mocks import setup_api_mocks, reset_deleted_users

pytest_plugins = (
    'utils.fixtures.users',
    'utils.fixtures.posts',
    'utils.fixtures.todos',
    'utils.fixtures.authentication',
)

# Global flag to track if we should use mocking
USE_MOCKING = False


def _check_api_accessibility():
    """Check if API is accessible or blocked by Cloudflare."""
    global USE_MOCKING
    
    # Check if we're in CI environment
    if os.getenv('CI') or os.getenv('GITHUB_ACTIONS'):
        try:
            headers = {'Authorization': f'Bearer {base_settings.test_user_token}'}
            response = httpx.get(f'{base_settings.api_url}posts', headers=headers, timeout=10)
            
            # Check if Cloudflare is blocking us
            if 'Just a moment' in response.text or 'cloudflare' in response.text.lower():
                USE_MOCKING = True
                return
        except httpx.RequestError:
            USE_MOCKING = True
            return


def pytest_configure(config):
    """Configure pytest - check API accessibility."""
    _check_api_accessibility()
    if USE_MOCKING:
        print("\n⚠️  API blocked by Cloudflare - running with mocked responses")


@pytest.fixture(autouse=True)
def reset_mock_state():
    """Reset mock state before each test."""
    reset_deleted_users()
    yield


@pytest.fixture(autouse=True)
def mock_api_if_needed(request):
    """Automatically mock API responses when Cloudflare blocks access."""
    if not USE_MOCKING:
        yield
        return
    
    with respx.mock(assert_all_called=False) as respx_mock:
        setup_api_mocks(respx_mock)
        yield respx_mock

