import allure

from models.order import Inventory, Order
from tests.assertions import assert_schema


@allure.feature("Магазин")
class TestStore:
    @allure.title("Остатки склада")
    def test_inventory(self, class_store_client):
        response, inventory = class_store_client.inventory()
        assert response.status_code == 200
        assert_schema(response.json(), Inventory)
        assert all(count >= 0 or name for name, count in inventory.root.items())

    @allure.title("Оформление заказа")
    def test_place_order(self, class_store_client):
        order = Order(quantity=3)
        response, created = class_store_client.place_order(order)
        assert response.status_code == 200
        assert_schema(response.json(), Order)
        assert created.id == order.id and created.quantity == 3 and created.status == "placed"
        class_store_client.delete_order(order.id)

    @allure.title("Получение заказа")
    def test_get_order(self, class_store_client, function_order):
        response = class_store_client.get_order(function_order.id)
        assert response.status_code == 200
        assert Order(**response.json()).pet_id == function_order.pet_id

    @allure.title("Удаление заказа")
    def test_delete_order(self, class_store_client):
        order = Order()
        class_store_client.place_order(order)
        class_store_client.get_order(order.id)
        assert class_store_client.delete_order(order.id).status_code == 200
        assert class_store_client.get_order(order.id, attempts=1).status_code == 404
