import pytest

from dogapi.client import DogClient


@pytest.mark.asyncio
async def test_breeds(event_loop):
    async with DogClient() as client:
        breeds = await client.breeds()
    assert "hound" in breeds


@pytest.mark.asyncio
async def test_random_images(event_loop):
    async with DogClient() as client:
        images = await client.random_images(3)
    assert len(images) == 3
