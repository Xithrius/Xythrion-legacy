import asyncio
import time
from typing import Any, Callable
import functools


def await_sync(func: Callable) -> Any:
    """
    Executor wrapper for different synchronous functions.

    Also times the function that is called.
    """

    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> tuple[Any, float]:
        sync_func = functools.partial(func, *args, **kwargs)

        t0 = time.time()
        output = await asyncio.get_event_loop().run_in_executor(None, sync_func)
        t1 = time.time()

        total_time = round((t1 - t0) * 1000, 2)

        return output, total_time

    return wrapper
