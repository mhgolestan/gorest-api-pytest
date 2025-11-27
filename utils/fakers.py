from random import choice, randint
from string import ascii_letters, digits
from faker import Faker
from datetime import datetime, timedelta


fake = Faker()


def random_number(start: int = 100, end: int = 1000) -> int:
    return randint(start, end)


def random_string(start: int = 9, end: int = 15) -> str:
    return ''.join(choice(ascii_letters + digits) for _ in range(randint(start, end)))


def random_email() -> str:
    return fake.email()


def random_gender() -> str:
    return choice(['male', 'female'])


def random_status() -> str:
    return choice(['active', 'inactive'])

def random_todo_status() -> str:
    return choice(['pending', 'completed'])


def random_due_date() -> str:
    """Generate a random due date in ISO format with timezone"""
    days_ahead = randint(1, 365)
    due_date = datetime.now() + timedelta(days=days_ahead)
    # Format: YYYY-MM-DDTHH:MM:SS.000+05:30
    return str(due_date.strftime("%Y-%m-%dT%H:%M:%S.000+05:30"))