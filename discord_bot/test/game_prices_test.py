import pytest
from unittest import mock
from discord_bot.test.utils import MockJSONResponse


@pytest.fixture()
def game_prices():
    # Mock away ITADApi module before testing
    with mock.patch("discord_bot.game_prices.api"):
        import discord_bot.game_prices as game_prices
        yield game_prices


def test_get_plain_from_title(game_prices):
    # Mock response
    game_prices.api.get_plain.return_value = MockJSONResponse({
        ".meta": {
            "match": "title",
            "active": True
        },
        "data": {
            "plain": "elitedangerous"
        }
    })

    # Should be able to successfully get plain ID from response obj
    plain = game_prices.get_id_from_game_title("Elite Dangerous")
    assert plain == "elitedangerous"


def test_get_plain_from_title_no_match(game_prices):
    game_prices.api.get_plain.return_value = MockJSONResponse({
        ".meta": {
            "match": False,
            "active": False
        },
        "data": []
    })

    # If no result is returned, plain ID should be None
    plain = game_prices.get_id_from_game_title("Not a real game")
    assert plain is None


def test_get_prices_single(game_prices):
    # Note: if the plain does not exist, we should just get an empty list from ITAD, so
    # no need to test the "does not exist" case.
    mock_resp_data = {
        "data": {
            "elitedangerous": {
                "list": [
                    {
                        "price_new": 8.35,
                        "price_old": 38.52,
                        "price_cut": 78,
                        "url": "https://www.gamebillet.com/elite-dangerous",
                        "shop": {
                            "id": "gamebillet",
                            "name": "GameBillet"
                        },
                        "drm": [
                            "steam"
                        ]
                    },
                    {
                        "price_new": 8.47,
                        "price_old": 38.67,
                        "price_cut": 78,
                        "url": "https://www.indiegala.com/store/game/elite-dangerous/359320?ref=itad",
                        "shop": {
                            "id": "indiegalastore",
                            "name": "IndieGala Store"
                        },
                        "drm": []
                    }
                ]
            },
            "oxygennotincluded": {
                "list": [
                    {
                        "price_new": 8.60,
                        "price_old": 34.48,
                        "price_cut": 75,
                        "url": "https://uk.gamesplanet.com/game/elite-dangerous-steam-key--4624-1?ref=itad",
                        "shop": {
                            "id": "gamesplanet",
                            "name": "GamesPlanet UK"
                        },
                        "drm": [
                            "steam"
                        ]
                    }
                ]
            }
        }
    }
    game_prices.api.get_prices.return_value = MockJSONResponse(mock_resp_data)

    # Should get results for all provided plains
    plains = ["elitedangerous", "oxygennotincluded"]
    prices = game_prices.get_prices_for_games(plains)

    for plain in plains:
        assert prices.get(plain) is not None

        for i, price_info in enumerate(prices[plain]):
            mock_resp_item = mock_resp_data["data"][plain]["list"][i]

            assert price_info.price_new == mock_resp_item["price_new"]
            assert price_info.price_old == mock_resp_item["price_old"]
            assert price_info.percent_off == mock_resp_item["price_cut"]
            assert price_info.url == mock_resp_item["url"]
