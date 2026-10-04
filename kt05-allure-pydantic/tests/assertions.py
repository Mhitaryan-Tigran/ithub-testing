import allure
from jsonschema import validate


@allure.step("Проверить пользователя")
def assert_user(actual, expected):
    for field in ("username", "first_name", "last_name", "email", "phone", "user_status"):
        assert getattr(actual, field) == getattr(expected, field), field


@allure.step("Проверить JSON-схему ответа")
def assert_schema(body, model):
    validate(instance=body, schema=model.model_json_schema(by_alias=True))
