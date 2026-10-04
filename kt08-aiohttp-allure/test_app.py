import json

import aiohttp
import allure
import pytest
from aiohttp import web

from app import get_json


@pytest.fixture
async def local_server(aiohttp_server):
    async def users(request):
        return web.json_response([{"id": 1, "name": "Tigran"}, {"id": 2, "name": "Maria"}])

    async def broken(request):
        return web.Response(status=500, text="boom")

    async def plain(request):
        return web.Response(text=json.dumps({"ok": True}), content_type="text/plain")

    app = web.Application()
    app.router.add_get("/users", users)
    app.router.add_get("/broken", broken)
    app.router.add_get("/plain", plain)
    return await aiohttp_server(app)


@allure.feature("get_json")
@allure.story("Публичные API")
@allure.title("Пост с jsonplaceholder")
@allure.description("Функция возвращает JSON-объект поста с нужными полями")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "smoke")
@pytest.mark.asyncio
async def test_get_post(event_loop):
    data = await get_json("https://jsonplaceholder.typicode.com/posts/1")
    allure.attach(json.dumps(data, ensure_ascii=False, indent=2), "ответ", allure.attachment_type.JSON)
    assert data["id"] == 1
    assert {"userId", "title", "body"} <= data.keys()


@allure.feature("get_json")
@allure.story("Публичные API")
@allure.title("Список пород Dog API")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api")
@pytest.mark.asyncio
async def test_get_dog_breeds(event_loop):
    data = await get_json("https://dog.ceo/api/breeds/list/all")
    assert data["status"] == "success"
    assert "hound" in data["message"]


@allure.feature("get_json")
@allure.story("Локальный сервер")
@allure.title("Список пользователей с тестового сервера")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("local")
@pytest.mark.asyncio
async def test_get_users_local(local_server):
    data = await get_json(str(local_server.make_url("/users")))
    assert [u["name"] for u in data] == ["Tigran", "Maria"]


@allure.feature("get_json")
@allure.story("Локальный сервер")
@allure.title("JSON с неверным Content-Type разбирается")
@allure.severity(allure.severity_level.MINOR)
@allure.tag("local", "edge")
@pytest.mark.asyncio
async def test_plain_content_type(local_server):
    assert await get_json(str(local_server.make_url("/plain"))) == {"ok": True}


@allure.feature("get_json")
@allure.story("Ошибки")
@allure.title("Ошибка сервера 500 превращается в исключение")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("negative")
@pytest.mark.asyncio
async def test_server_error(local_server):
    with pytest.raises(aiohttp.ClientResponseError) as error:
        await get_json(str(local_server.make_url("/broken")))
    assert error.value.status == 500


@allure.feature("get_json")
@allure.story("Ошибки")
@allure.title("Своя сессия не закрывается функцией")
@allure.severity(allure.severity_level.MINOR)
@allure.tag("local")
@pytest.mark.asyncio
async def test_external_session(local_server):
    async with aiohttp.ClientSession() as session:
        await get_json(str(local_server.make_url("/users")), session=session)
        assert not session.closed
