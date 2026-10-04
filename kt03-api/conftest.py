import random

import pytest

from base_request import BASE_URL_PETSTORE, BaseRequest


@pytest.fixture(scope="session")
def api():
    return BaseRequest(BASE_URL_PETSTORE)


@pytest.fixture
def username():
    return f"tigran_qa_{random.randint(100000, 999999)}"


@pytest.fixture
def order_id():
    return random.randint(5, 9)
