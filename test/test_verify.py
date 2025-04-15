from unittest.mock import patch

import pytest

from verify import verify
from verify_modes import VerifyMode


def test_verify_crash_mode_pass():
    with patch("verify.ASSERT_MODE", VerifyMode.CRASH):
        # Should not raise an exception
        verify(lambda: True, "This should pass")


def test_verify_crash_mode_fail():
    with patch("verify.ASSERT_MODE", VerifyMode.CRASH):
        # Should raise AssertionError
        with pytest.raises(AssertionError, match="This should fail"):
            verify(lambda: False, "This should fail")


def test_verify_log_mode_pass():
    with patch("verify.ASSERT_MODE", VerifyMode.LOG):
        # Should not log anything
        with patch("verify.logger.critical") as mock_log:
            verify(lambda: True, "This should pass")
            mock_log.assert_not_called()


def test_verify_log_mode_fail():
    with patch("verify.ASSERT_MODE", VerifyMode.LOG):
        # Should log a critical error
        with patch("verify.logger.critical") as mock_log:
            verify(lambda: False, "This should fail")
            mock_log.assert_called_once_with("Assertion failed: This should fail")


def test_verify_skip_mode_pass():
    with patch("verify.ASSERT_MODE", VerifyMode.SKIP):
        # Should skip verification completely
        verify(lambda: True, "This should be skipped")


def test_verify_skip_mode_fail():
    with patch("verify.ASSERT_MODE", VerifyMode.SKIP):
        # Should skip verification even for failing condition
        verify(lambda: False, "This should be skipped")


def test_verify_with_bool_instead_of_callable():
    with patch("verify.ASSERT_MODE", VerifyMode.CRASH):
        # Will raise TypeError because True is not callable
        with pytest.raises(TypeError):
            verify(True, "Boolean passed directly instead of callable")
