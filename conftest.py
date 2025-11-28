pytest_plugins = (
    'utils.fixtures.users',
    'utils.fixtures.posts',
    'utils.fixtures.todos',
)

import os
import pytest
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@pytest.fixture(scope="session", autouse=True)
def setup_environment():
    """Ensure environment variables are set"""
    base_url = os.getenv("base_url") or os.getenv("BASE_URL")
    test_token = os.getenv("test_user_token") or os.getenv("TEST_USER_TOKEN")
    print(f"BASE_URL: {base_url}")
    if not base_url:
        pytest.skip("BASE_URL environment variable not set")
    if not test_token:
        pytest.skip("TEST_USER_TOKEN environment variable not set")