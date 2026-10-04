import time

import allure

from models.order import Inventory, Order
from models.user import ApiResponse, User


class APIClient:
    def __init__(self, client):
        self.client = client


class UsersClient(APIClient):
    @allure.step("Создать пользователя")
    def create_user(self, user):
        response = self.client.post("/user", json=user.model_dump(by_alias=True))
        return response, ApiResponse(**response.json())

    @allure.step("Получить пользователя {username}")
    def get_user(self, username, attempts=6):
        response = None
        for attempt in range(attempts):
            response = self.client.get(f"/user/{username}")
            if response.status_code == 200:
                break
            time.sleep(0.5 * (attempt + 1))
        return response

    @allure.step("Обновить пользователя")
    def update_user(self, user):
        return self.client.put(f"/user/{user.username}", json=user.model_dump(by_alias=True))

    @allure.step("Удалить пользователя {username}")
    def delete_user(self, username):
        return self.client.delete(f"/user/{username}")


class StoreClient(APIClient):
    @allure.step("Получить остатки склада")
    def inventory(self):
        response = self.client.get("/store/inventory")
        return response, Inventory(response.json())

    @allure.step("Оформить заказ")
    def place_order(self, order):
        response = self.client.post("/store/order", json=order.model_dump(by_alias=True))
        return response, Order(**response.json())

    @allure.step("Получить заказ {order_id}")
    def get_order(self, order_id, attempts=6):
        response = None
        for attempt in range(attempts):
            response = self.client.get(f"/store/order/{order_id}")
            if response.status_code == 200:
                break
            time.sleep(0.5 * (attempt + 1))
        return response

    @allure.step("Удалить заказ {order_id}")
    def delete_order(self, order_id):
        return self.client.delete(f"/store/order/{order_id}")
