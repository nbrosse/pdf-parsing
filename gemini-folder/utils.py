import asyncio
from typing import TypeVar, Any, Coroutine

T = TypeVar("T")


async def run_jobs(
    jobs: list[Coroutine[Any, Any, T]],
    show_progress: bool = False,
    workers: int = 4,
    desc: str | None = None,
) -> list[T]:
    """Run jobs.

    Args:
        jobs (List[Coroutine]):
            List of jobs to run.
        show_progress (bool):
            Whether to show progress bar.

    Returns:
        List[Any]:
            List of results.
    """
    semaphore = asyncio.Semaphore(workers)

    async def worker(job: Coroutine) -> Any:
        async with semaphore:
            return await job

    pool_jobs = [worker(job) for job in jobs]

    if show_progress:
        from tqdm.asyncio import tqdm_asyncio

        results = await tqdm_asyncio.gather(*pool_jobs, desc=desc)
    else:
        results = await asyncio.gather(*pool_jobs)

    return results


def asyncio_run(coro: Coroutine) -> Any:
    """Gets an existing event loop to run the coroutine.

    If there is no existing event loop, creates a new one.
    """
    try:
        # Check if there's an existing event loop
        loop = asyncio.get_event_loop()

        # If we're here, there's an existing loop but it's not running
        return loop.run_until_complete(coro)

    except RuntimeError as e:
        # If we can't get the event loop, we're likely in a different thread, or its already running
        try:
            return asyncio.run(coro)
        except RuntimeError as e:
            raise RuntimeError(
                "Detected nested async. Please use nest_asyncio.apply() to allow nested event loops."
                "Or, use async entry methods like `aquery()`, `aretriever`, `achat`, etc."
            )