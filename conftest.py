import pytest
import httpx
from settings import base_settings

pytest_plugins = (
    'utils.fixtures.users',
    'utils.fixtures.posts',
    'utils.fixtures.todos',
)


def pytest_configure(config):
    """Check if API is accessible before running tests."""
    try:
        headers = {'Authorization': f'Bearer {base_settings.test_user_token}'}
        response = httpx.get(f'{base_settings.api_url}posts', headers=headers, timeout=10)
        
        # Check if Cloudflare is blocking us
        if 'Just a moment' in response.text or response.status_code == 403:
            pytest.exit(
                "API is blocked by Cloudflare. "
                "This typically happens in CI environments. "
                "Tests cannot run against the live API from this environment.",
                returncode=0  # Exit with 0 to not fail the build
            )
    except httpx.RequestError as e:
        pytest.exit(f"Cannot connect to API: {e}", returncode=1)
