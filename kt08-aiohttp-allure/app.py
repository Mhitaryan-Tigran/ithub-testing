import aiohttp


async def get_json(url, session=None, timeout=15):
    own = session is None
    session = session or aiohttp.ClientSession()
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=timeout)) as response:
            response.raise_for_status()
            return await response.json(content_type=None)
    finally:
        if own:
            await session.close()
