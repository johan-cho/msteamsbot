"""Threader helper function."""
from threading import Thread
from typing import Callable


def threader(func: Callable, join: bool = False, *args, **kwargs) -> None:
    """Threads a function.

    Args:
        func: The function to thread.
        join: Whether to join the thread.
        args: The arguments to pass to the function.
        kwargs: The keyword arguments to pass to the function.
    """

    job_thread = Thread(target=func, args=args, kwargs=kwargs)
    job_thread.start()
    if join:
        job_thread.join()
