# tests/test_fakeapi.py
"""Module to test fake api usage.

Meant to serve as template in case the package uses non-local database.
"""
import pytest


class FakeAPI:
    """Fake API."""

    url = "http://localhost:5000/"

    @classmethod
    def create(cls):
        """Expensive operation to create API."""
        return FakeAPI()

    def shutdown(self):
        """Expensive shutdown operation."""
        return "expensive shutdown"


@pytest.fixture(scope="session")
def fake_api():
    """Yield api inerface when needed.

    Scope set to session, to only create once per test session.

    Yields
    ------
    FakeAPI
        FakeAPI instance using a localhost as url.
    """
    api = FakeAPI.create()
    yield api
    api.shutdown()
