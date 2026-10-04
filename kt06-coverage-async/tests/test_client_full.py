import httpx
import pytest

from dogapi.client import BreedNotFound, DogClient, breed_label


@pytest.mark.asyncio
async def test_sub_breeds(event_loop):
    async with DogClient() as client:
        assert "afghan" in await client.sub_breeds("Hound")


@pytest.mark.asyncio
async def test_random_images_for_breed(event_loop):
    async with DogClient() as client:
        images = await client.random_images(2, breed="pug")
    assert all("/pug/" in url for url in images)


@pytest.mark.asyncio
@pytest.mark.parametrize("count", [0, 51])
async def test_count_out_of_range(event_loop, count):
    async with DogClient() as client:
        with pytest.raises(ValueError):
            await client.random_images(count)


@pytest.mark.asyncio
async def test_unknown_breed(event_loop):
    async with DogClient() as client:
        with pytest.raises(BreedNotFound):
            await client.sub_breeds("nosuchbreed")


@pytest.mark.asyncio
async def test_images_for_many_in_parallel(event_loop):
    async with DogClient() as client:
        counts = await client.images_for_many(["pug", "husky", "nosuchbreed"])
    assert counts["pug"] > 0 and counts["husky"] > 0
    assert counts["nosuchbreed"] is None


@pytest.mark.asyncio
async def test_api_error_status(event_loop):
    transport = httpx.MockTransport(lambda request: httpx.Response(200, json={"status": "error", "message": "boom"}))
    async with DogClient(transport=transport) as client:
        with pytest.raises(RuntimeError):
            await client.breeds()


@pytest.mark.asyncio
async def test_server_error(event_loop):
    transport = httpx.MockTransport(lambda request: httpx.Response(503))
    async with DogClient(transport=transport) as client:
        with pytest.raises(httpx.HTTPStatusError):
            await client.breeds()


def test_breed_label():
    assert breed_label("hound", "afghan") == "Afghan Hound"
    assert breed_label("pug") == "Pug"
