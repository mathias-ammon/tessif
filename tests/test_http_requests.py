# tests/test_http_requests.py
"""Module to test https request calls using the request package.

Targets are mostly mocked using pytest-mock plugin
(poetry add --def pytest-mock).

Meant to serve as template in case the package uses url based api calls.
"""
# third party packages
import pytest
import requests


def request_url(url):
    """with wrapper to requests.get."""

    try:
        with requests.get(url) as response:
            response.raise_for_status()
            return response

    except requests.RequestException:
        message = "Error: request_url failed."
        return message


@pytest.fixture
def mock_requests_get(mocker):
    mock = mocker.patch("requests.get")
    mock.return_value.__enter__.return_value.json.return_value = {
        "title": "Lorem Ipsum",
        "extract": "Lorem ipsum dolor sit amet",
    }
    return mock


@pytest.fixture
def request_rnd_wiki_artcl():
    """Tries reaching the wikipedia site to get a random article"""

    API_URL = "https://en.wikipedia.org/api/rest_v1/page/random/summary"
    response = request_url(API_URL)
    json_response = response.json()

    return json_response


def test_mock_gets_called(mock_requests_get, request_rnd_wiki_artcl):
    """Assert the requests.get was actually called.

    random_wiki_article gets called by fixutre wrap around mock object so
    the mock object is "requests.get" instead of the url.
    Fixture order is implortant!

    Since the data content is not of importance calling the fixture alone
    suffices.
    """
    assert mock_requests_get.called


def test_mock_result_inspection(mock_requests_get, request_rnd_wiki_artcl):
    """Test successful mock result inspection."""

    http_json_response = request_rnd_wiki_artcl
    assert "Lorem Ipsum" in http_json_response["title"]


def test_mock_param_call_inspection(mock_requests_get, request_rnd_wiki_artcl):
    """Assert the requests.get was called properly.

    random_wiki_article gets called by fixutre wrap around mock object so
    the mock object is "requests.get" instead of the url.
    Fixture order is implortant!

    Since the data content is not of importance calling the fixture alone
    suffices.
    """
    args, _ = mock_requests_get.call_args
    assert "en.wikipedia.org" in args[0]


def test_fail_on_request_error(mock_requests_get, request_rnd_wiki_artcl):
    """Test on failing the https request."""
    mock_requests_get.side_effect = requests.RequestException

    API_URL = "https://en.wikipedia.org/api/rest_v1/page/random/summary"
    mock_response = request_url(API_URL)

    assert "Error" in mock_response


# continue with end to end tests and actual connectivity tests
# continue with data base FAKES
