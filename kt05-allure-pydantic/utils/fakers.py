from random import choice, randint
from string import ascii_letters, ascii_lowercase, digits


def random_number(start=100, end=1000):
    return randint(start, end)


def random_string(start=9, end=15):
    return "".join(choice(ascii_letters + digits) for _ in range(randint(start, end)))


def random_username():
    return "qa_" + "".join(choice(ascii_lowercase + digits) for _ in range(10))


def random_email():
    return f"{random_username()}@example.com"
