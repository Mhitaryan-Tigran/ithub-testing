import threading

import aiosqlite
import pytest

from tasks import add_student, compute_square, create_table, fetch_post, fetch_user, heavy_async_job, run_in_thread


@pytest.mark.asyncio
async def test_future_resolves(event_loop):
    future = event_loop.create_task(compute_square(7))
    assert await future == 49


@pytest.mark.asyncio
async def test_future_rejects(event_loop):
    with pytest.raises(ValueError, match="positive"):
        await event_loop.create_task(fetch_user(0))


@pytest.mark.asyncio
async def test_http_request(event_loop):
    post = await fetch_post(1)
    assert post["id"] == 1
    assert {"userId", "title", "body"} <= post.keys()


@pytest.mark.asyncio
async def test_database_insert(event_loop, tmp_path):
    async with aiosqlite.connect(tmp_path / "college.db") as db:
        await create_table(db)
        new_id = await add_student(db, "Тигран", 5)
        async with db.execute("SELECT name, grade FROM students WHERE id = ?", (new_id,)) as cursor:
            row = await cursor.fetchone()
    assert row == ("Тигран", 5)


@pytest.mark.asyncio
async def test_run_in_separate_thread(event_loop):
    main_thread = threading.get_ident()
    seen = {}

    async def job(n):
        seen["thread"] = threading.get_ident()
        return await heavy_async_job(n)

    import tasks
    original = tasks.heavy_async_job
    tasks.heavy_async_job = job
    try:
        result = await run_in_thread(1000)
    finally:
        tasks.heavy_async_job = original
    assert result == sum(range(1000))
    assert seen["thread"] != main_thread
