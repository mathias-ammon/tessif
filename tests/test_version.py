# tests/test_version.py

from tessif import __version__


def test_verssion_access():
    assert __version__ == "0.0.1"
