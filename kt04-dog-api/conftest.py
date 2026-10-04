import pytest

from base_request import BaseRequest

BASE_URL_DOG = "https://dog.ceo/api"


@pytest.fixture(scope="session")
def api():
    return BaseRequest(BASE_URL_DOG)


@pytest.fixture(scope="session")
def all_breeds(api):
    return api.get("breeds/list/all").json()["message"]
