from typing import Callable

from loguru import logger

from verify_modes import ASSERT_MODE, VerifyMode


def verify(cond: Callable, message: str = ""):
    """The condition_func should return a boolean value. Note it needs to be a callable not a boolean value itself.
    In front of your condition you could do lambda: <condition> to make it a callable."""
    if ASSERT_MODE == VerifyMode.SKIP:
        return
    result = cond()
    if not result:
        if ASSERT_MODE == VerifyMode.LOG:
            logger.critical(f"Assertion failed: {message}")
        elif ASSERT_MODE == VerifyMode.CRASH:
            raise AssertionError(message)
