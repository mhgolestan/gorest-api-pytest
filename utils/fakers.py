from random import choice, randint
from string import ascii_letters, digits
from faker import Faker


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