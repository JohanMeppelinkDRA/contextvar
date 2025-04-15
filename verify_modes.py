import os
from enum import Enum


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
