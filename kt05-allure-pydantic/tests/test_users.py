import allure
import pytest

from models.user import ApiResponse, User
from tests.assertions import assert_schema, assert_user


@allure.feature("Пользователи")
class TestUsers:
    @allure.title("Создание пользователя")
    def test_create_user(self, class_users_client):
        user = User()
        response, body = class_users_client.create_user(user)
        assert response.status_code == 200
        assert body.code == 200
        assert_schema(response.json(), ApiResponse)
        class_users_client.delete_user(user.username)

    @allure.title("Получение пользователя")
    def test_get_user(self, class_users_client, function_user):
        response = class_users_client.get_user(function_user.username)
        assert response.status_code == 200
        assert_schema(response.json(), User)
        assert_user(User(**response.json()), function_user)

    @allure.title("Обновление пользователя")
    def test_update_user(self, class_users_client, function_user):
        changed = function_user.model_copy(update={"first_name": "Tiko", "phone": "+71111111111"})
        assert class_users_client.update_user(changed).status_code == 200
        response = class_users_client.get_user(function_user.username)
        assert_user(User(**response.json()), changed)

    @allure.title("Удаление пользователя")
    def test_delete_user(self, class_users_client):
        user = User()
        class_users_client.create_user(user)
        class_users_client.get_user(user.username)
        assert class_users_client.delete_user(user.username).status_code == 200
        assert class_users_client.get_user(user.username, attempts=1).status_code == 404

    @allure.title("Модель отклоняет некорректную почту")
    def test_model_rejects_bad_email(self):
        with pytest.raises(ValueError):
            User(email="not-an-email")
