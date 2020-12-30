import pytest
from unittest import mock
from discord_bot.itad_api import ITADApi


@pytest.fixture
def mock_requests():
    with mock.patch("discord_bot.itad_api.requests") as mock_requests:
        yield mock_requests


@pytest.fixture
def mock_api_key():
    with mock.patch("discord_bot.config.ITAD_API_KEY", "TESTAPIKEY") as api_key:
        yield api_key


def test_get_plain_sends_api_key(mock_requests, mock_api_key):
    """Check that we're sending the API key with our requests. We should be using the same logic to
    do this for all requests, so no need to re-test for every request.
    """
    itad_api = ITADApi()

    itad_api.get_plain("Elite Dangerous")

    mock_requests.get.assert_called_once()

    url, payload = mock_requests.get.call_args[0]
    assert payload["key"] == mock_api_key
