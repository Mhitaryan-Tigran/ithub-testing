import asyncio

import httpx

BASE_URL = "https://dog.ceo/api"


class BreedNotFound(Exception):
    pass


class DogClient:
    def __init__(self, base_url=BASE_URL, transport=None, timeout=15.0):
        self._client = httpx.AsyncClient(base_url=base_url, transport=transport, timeout=timeout)

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        await self._client.aclose()

    async def _get(self, path):
        response = await self._client.get(path)
        if response.status_code == 404:
            raise BreedNotFound(response.json().get("message", path))
        response.raise_for_status()
        body = response.json()
        if body.get("status") != "success":
            raise RuntimeError(body)
        return body["message"]

    async def breeds(self):
        return await self._get("/breeds/list/all")

    async def sub_breeds(self, breed):
        return await self._get(f"/breed/{breed.lower()}/list")

    async def random_images(self, count=1, breed=None):
        if not 1 <= count <= 50:
            raise ValueError("count must be between 1 and 50")
        path = f"/breed/{breed.lower()}/images/random/{count}" if breed else f"/breeds/image/random/{count}"
        return await self._get(path)

    async def images_for_many(self, breeds):
        results = await asyncio.gather(*(self._get(f"/breed/{b}/images") for b in breeds), return_exceptions=True)
        return {b: (len(r) if isinstance(r, list) else None) for b, r in zip(breeds, results)}


def breed_label(breed, sub=None):
    return f"{sub.title()} {breed.title()}" if sub else breed.title()
