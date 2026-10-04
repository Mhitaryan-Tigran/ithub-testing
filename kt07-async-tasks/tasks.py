import asyncio

import aiohttp
import aiosqlite


async def compute_square(x, delay=0.01):
    await asyncio.sleep(delay)
    return x * x


async def fetch_user(user_id):
    await asyncio.sleep(0.01)
    if user_id <= 0:
        raise ValueError("user_id must be positive")
    return {"id": user_id}


async def fetch_post(post_id, session=None):
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
    own = session is None
    session = session or aiohttp.ClientSession()
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as response:
            response.raise_for_status()
            return await response.json()
    finally:
        if own:
            await session.close()


async def create_table(db):
    await db.execute("CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY, name TEXT NOT NULL, grade INTEGER)")
    await db.commit()


async def add_student(db, name, grade):
    cursor = await db.execute("INSERT INTO students (name, grade) VALUES (?, ?)", (name, grade))
    await db.commit()
    return cursor.lastrowid


async def heavy_async_job(n):
    await asyncio.sleep(0.01)
    return sum(range(n))


def _run_in_new_loop(coro_factory, *args):
    return asyncio.run(coro_factory(*args))


async def run_in_thread(n):
    return await asyncio.to_thread(_run_in_new_loop, heavy_async_job, n)
