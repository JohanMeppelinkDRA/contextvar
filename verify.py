import os
from enum import Enum
from typing import Callable

from loguru import logger


class VerifyMode(Enum):
    CRASH = "crash"  # Raise exception on failure
    LOG = "log"  # Log critical error on failure
    SKIP = "skip"  # Skip condition evaluation


VERIFY_MODE = VerifyMode.CRASH
try:
    ASSERT_MODE = VerifyMode(os.environ.get("ASSERT_MODE", VERIFY_MODE.value))
except ValueError:
    ASSERT_MODE = VERIFY_MODE  # Fallback to default on invalid input

if not __debug__:  # True when running with -O/-OO
    ASSERT_MODE = VerifyMode.SKIP  # Auto-disable in optimized mode


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
