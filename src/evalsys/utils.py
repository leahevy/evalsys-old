import asyncio
import concurrent.futures
import typing

import aiofiles


class ThreadPoolExecutor(concurrent.futures.ThreadPoolExecutor):
    async def call(self, callback, *args, **kwargs):
        return await asyncio.wrap_future(self.submit(callback, *args, **kwargs))


_async_pool = None


def bgpool_run_async(fun):
    global _async_pool
    if _async_pool is None:
        _async_pool = ThreadPoolExecutor()
    return _async_pool.call(fun)


def bgpool_run_sync(fun):
    return asyncio.run(bgpool_run_async(fun))


async def _internal_coro(coro: typing.Coroutine[typing.Any, typing.Any, None]):
    tasks_before = asyncio.all_tasks()
    await coro
    tasks_after = [task for task in asyncio.all_tasks() if task not in tasks_before]
    if tasks_after:
        await asyncio.wait(tasks_after)


def async_loop_start(coro: typing.Coroutine[typing.Any, typing.Any, None]):
    asyncio.run(_internal_coro(coro))