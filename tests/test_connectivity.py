# tests/test_connectivity.py
"""Module for testing connectivity.

Meant to serve as template in case outgoing connections are to be tested.
"""
import pytest
import requests


def request_url(url):
    """With wrapper to requests.get."""
    try:
        with requests.get(url) as response:
            response.raise_for_status()
            return response

    except requests.RequestException:
        message = "Error: request_url failed."
        return message


@pytest.fixture
def request_random_wiki_article():
    """Try reaching the wikipedia site to get a random article."""
    api_url = "https://en.wikipedia.org/api/rest_v1/page/random/summary"
    response = request_url(api_url)

    return response


@pytest.mark.con
def test_wikipedia_connectivity(request_random_wiki_article):
    """Try reaching the wikipedia site to get a random article."""
    # pylint: disable=redefined-outer-name
    # disabled here, sind redefinition is how fixtures work

    answer = request_random_wiki_article
    print(answer)
    assert "Error" not in answer
