import httpx
import pytest
import pytest_asyncio

import main

API = "http://test/api"
USER = {"username": "testuser", "password": "testpass123", "email": "testuser@example.com", "name": "Test User"}


@pytest.fixture(autouse=True)
def clean_state():
    main.USERS.clear()
    main.TOKENS.clear()


@pytest_asyncio.fixture
async def client():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url=API) as c:
        yield c


async def register(client, **extra):
    return await client.post("/register", json=USER | extra)


async def token(client):
    await register(client)
    response = await client.post("/login", json={"username": USER["username"], "password": USER["password"]})
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


@pytest.mark.asyncio
async def test_register(event_loop, client):
    response = await register(client)
    assert response.status_code == 201
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_register_duplicate(event_loop, client):
    await register(client)
    assert (await register(client)).status_code == 409


@pytest.mark.asyncio
@pytest.mark.parametrize("field,value", [("email", "not-an-email"), ("password", "short"), ("username", "a b"), ("name", "")])
async def test_register_validation(event_loop, client, field, value):
    assert (await register(client, **{field: value})).status_code == 422


@pytest.mark.asyncio
async def test_login(event_loop, client):
    await register(client)
    response = await client.post("/login", json={"username": "testuser", "password": "testpass123"})
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_login_wrong_password(event_loop, client):
    await register(client)
    response = await client.post("/login", json={"username": "testuser", "password": "wrong-pass"})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_case_insensitive_username(event_loop, client):
    await register(client)
    assert (await client.post("/login", json={"username": "TestUser", "password": "testpass123"})).status_code == 200


@pytest.mark.asyncio
async def test_get_profile(event_loop, client):
    response = await client.get("/profile", headers=await token(client))
    assert response.status_code == 200
    assert response.json() == {"username": "testuser", "email": "testuser@example.com", "name": "Test User"}


@pytest.mark.asyncio
@pytest.mark.parametrize("headers", [{}, {"Authorization": "Bearer nope"}, {"Authorization": "Basic abc"}])
async def test_profile_requires_token(event_loop, client, headers):
    assert (await client.get("/profile", headers=headers)).status_code == 401


@pytest.mark.asyncio
async def test_update_profile(event_loop, client):
    headers = await token(client)
    response = await client.patch("/profile", json={"email": "testuser2@example.com", "name": "Test User 2"}, headers=headers)
    assert response.status_code == 200
    assert (await client.get("/profile", headers=headers)).json() == {"username": "testuser", "email": "testuser2@example.com", "name": "Test User 2"}


@pytest.mark.asyncio
async def test_update_profile_partial(event_loop, client):
    headers = await token(client)
    await client.patch("/profile", json={"name": "Только имя"}, headers=headers)
    body = (await client.get("/profile", headers=headers)).json()
    assert body["name"] == "Только имя" and body["email"] == USER["email"]


@pytest.mark.asyncio
async def test_update_profile_rejects_bad_email(event_loop, client):
    assert (await client.patch("/profile", json={"email": "bad"}, headers=await token(client))).status_code == 422


@pytest.mark.asyncio
async def test_password_not_exposed(event_loop, client):
    body = (await client.get("/profile", headers=await token(client))).json()
    assert "password" not in body and "hash" not in body


@pytest.mark.asyncio
async def test_logout_revokes_token(event_loop, client):
    headers = await token(client)
    assert (await client.post("/logout", headers=headers)).status_code == 204
    assert (await client.get("/profile", headers=headers)).status_code == 401
