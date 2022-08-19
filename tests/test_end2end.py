# tests/test_end2end.py
"""Module for end2end testing.

Meant to serve as template in case end2end tesing is sensible.
Uses pytest markers to require manual test inclusion.
"""
import pytest


@pytest.mark.e2e
def test_unix_specifics():
    """Test unix specific things."""
    # pylint: disable=comparison-of-constants
    # remove this, once the test does someting meaningfull
    assert "unix" in "Do some unix tests"


@pytest.mark.e2e
def test_windows_specifics():
    """Test windows specific things."""
    # pylint: disable=comparison-of-constants
    # remove this, once the test does someting meaningful
    assert "unix" not in "Do some windows tests"
