import pytest

from clients.http_client import get_http_client
from clients.petstore import StoreClient, UsersClient
from models.order import Order
from models.user import User


@pytest.fixture(scope="class")
def class_users_client():
    with get_http_client() as client:
        yield UsersClient(client)


@pytest.fixture(scope="class")
def class_store_client():
    with get_http_client() as client:
        yield StoreClient(client)


@pytest.fixture
def function_user(class_users_client):
    user = User()
    class_users_client.create_user(user)
    yield user
    class_users_client.delete_user(user.username)


@pytest.fixture
def function_order(class_store_client):
    order = Order()
    class_store_client.place_order(order)
    yield order
    class_store_client.delete_order(order.id)
