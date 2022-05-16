from unittest.mock import MagicMock

from currency.models import Rate
from currency.tasks import parse_monobank, parse_vkurse


def test_parse_monobank(mocker):
    response_json = [
        {"currencyCodeA": 840, "currencyCodeB": 980, "date": 1652649007, "rateBuy": 29.5, "rateSell": 31.5},
        {"currencyCodeA": 978, "currencyCodeB": 980, "date": 1652689807, "rateBuy": 30.68, "rateSell": 32.9804},
        {"currencyCodeA": 978, "currencyCodeB": 840, "date": 1652649007, "rateBuy": 1.03, "rateSell": 1.05},
    ]
    request_get_mock = mocker.patch(
        'requests.get',
        return_value=MagicMock(json=lambda: response_json),
    )

    # first request
    rate_initial_count = Rate.objects.count()
    parse_monobank()
    assert Rate.objects.count() == rate_initial_count + 3
    assert request_get_mock.call_count == 1

    # request with no changes
    parse_monobank()
    assert Rate.objects.count() == rate_initial_count + 3
    assert request_get_mock.call_count == 2
    assert request_get_mock.call_args[0] == ('https://api.monobank.ua/bank/currency',)
    assert request_get_mock.call_args[1] == {}

    # request with changes
    response_json = [
        {"currencyCodeA": 840, "currencyCodeB": 980, "date": 1652649008, "rateBuy": 29.55, "rateSell": 31.52},
        {"currencyCodeA": 978, "currencyCodeB": 980, "date": 1652689807, "rateBuy": 30.68, "rateSell": 32.9804},
        {"currencyCodeA": 978, "currencyCodeB": 840, "date": 1652649007, "rateBuy": 1.03, "rateSell": 1.05},
    ]
    request_get_mock_2 = mocker.patch(
        'requests.get',
        return_value=MagicMock(json=lambda: response_json),
    )
    assert request_get_mock_2.call_count == 0
    parse_monobank()
    assert Rate.objects.count() == rate_initial_count + 4
    assert request_get_mock_2.call_count == 1


def test_parse_vkurse(mocker):
    response_json = {
        "Dollar": {
            "buy": "32.15",
            "sale": "34.70"
        },
        "Euro": {
            "buy": "35.50",
            "sale": "36.30"
        },
        "Rub": {
            "buy": "00.00",
            "sale": "00.00"
        }
    }
    request_get_mock = mocker.patch(
        'requests.get',
        return_value=MagicMock(json=lambda: response_json),
    )

    # first request
    rate_initial_count = Rate.objects.count()
    parse_vkurse()
    assert Rate.objects.count() == rate_initial_count + 2
    assert request_get_mock.call_count == 1

    # request with no changes
    parse_vkurse()
    assert Rate.objects.count() == rate_initial_count + 2
    assert request_get_mock.call_count == 2
    assert request_get_mock.call_args[0] == ('http://www.vkurse.dp.ua/course.json',)
    assert request_get_mock.call_args[1] == {}

    # request with changes
    response_json = {
        "Dollar": {
            "buy": "33.15",
            "sale": "35.70"
        }
    }
    request_get_mock_2 = mocker.patch(
        'requests.get',
        return_value=MagicMock(json=lambda: response_json),
    )
    assert request_get_mock_2.call_count == 0
    parse_vkurse()
    assert Rate.objects.count() == rate_initial_count + 3
    assert request_get_mock_2.call_count == 1
