from unittest.mock import MagicMock

from currency.models import Rate, Source
from currency.tasks import parse_credit_agricole, parse_minfin_avarage, parse_monobank, parse_oschadbank, \
    parse_privatbank, parse_vkurse


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

    # request with changes Source.DoesNotExist
    Source.objects.filter(name='MonoBank').delete()
    response_json = [
        {"currencyCodeA": 840, "currencyCodeB": 980, "date": 1652649008, "rateBuy": 29.55, "rateSell": 31.52},
        {"currencyCodeA": 978, "currencyCodeB": 980, "date": 1652689807, "rateBuy": 30.68, "rateSell": 32.9804},
        {"currencyCodeA": 978, "currencyCodeB": 840, "date": 1652649007, "rateBuy": 1.03, "rateSell": 1.05},
        {"currencyCodeA": 444, "currencyCodeB": 840, "date": 1652649007, "rateBuy": 1.03, "rateSell": 1.05},
    ]
    request_get_mock_2 = mocker.patch(
        'requests.get',
        return_value=MagicMock(json=lambda: response_json),
    )
    assert request_get_mock_2.call_count == 0
    parse_monobank()
    assert Rate.objects.count() == rate_initial_count + 2
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


def test_parse_privatbank(mocker):
    response_json = [
        {"ccy": "USD", "base_ccy": "UAH", "buy": "29.25490", "sale": "32.05128"},
        {"ccy": "EUR", "base_ccy": "UAH", "buy": "30.47920", "sale": "33.44482"},
        {"ccy": "RUR", "base_ccy": "UAH", "buy": "0.32000", "sale": "0.35001"},
        {"ccy": "BTC", "base_ccy": "USD", "buy": "28982.9116", "sale": "32033.7444"}
    ]
    request_get_mock = mocker.patch(
        'requests.get',
        return_value=MagicMock(json=lambda: response_json),
    )

    # first request
    rate_initial_count = Rate.objects.count()
    parse_privatbank()
    assert Rate.objects.count() == rate_initial_count + 3
    assert request_get_mock.call_count == 1

    # request with no changes
    parse_privatbank()
    assert Rate.objects.count() == rate_initial_count + 3
    assert request_get_mock.call_count == 2
    assert request_get_mock.call_args[0] == ('https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11',)
    assert request_get_mock.call_args[1] == {}

    # request with changes Source.DoesNotExist
    Source.objects.filter(name='PrivatBank').delete()
    response_json = [
        {"ccy": "USD", "base_ccy": "UAH", "buy": "29.2550", "sale": "32.05129"},
        {"ccy": "EUR", "base_ccy": "UAH", "buy": "30.47920", "sale": "33.44482"},
        {"ccy": "RUR", "base_ccy": "UAH", "buy": "0.32000", "sale": "0.35001"},
        {"ccy": "BTC", "base_ccy": "USD", "buy": "28982.9116", "sale": "32033.7444"},
    ]
    request_get_mock_2 = mocker.patch(
        'requests.get',
        return_value=MagicMock(json=lambda: response_json),
    )
    assert request_get_mock_2.call_count == 0
    parse_privatbank()
    assert Rate.objects.count() == rate_initial_count + 1
    assert request_get_mock_2.call_count == 1


def test_parse_oschadbank(mocker):
    with open('app/tests/file_html/oschadbank.txt', 'r') as file:
        value = file.read()
    request_get_mock = mocker.patch('requests.get', return_value=MagicMock(text=value))

    # first request
    rate_initial_count = Rate.objects.count()
    parse_oschadbank()
    assert Rate.objects.count() == rate_initial_count + 2
    assert request_get_mock.call_count == 1

    # request with no changes
    parse_oschadbank()
    assert Rate.objects.count() == rate_initial_count + 2
    assert request_get_mock.call_count == 2
    assert request_get_mock.call_args[0] == ('https://www.oschadbank.ua/currency-rate',)
    assert request_get_mock.call_args[1] == {}

    # request with changes Source.DoesNotExist
    Source.objects.filter(name='OschadBank').delete()
    with open('app/tests/file_html/oschadbank2.txt', 'r') as file:
        value = file.read()
    request_get_mock_2 = mocker.patch('requests.get', return_value=MagicMock(text=value))

    assert request_get_mock_2.call_count == 0
    parse_oschadbank()
    assert Rate.objects.count() == rate_initial_count + 2
    assert request_get_mock_2.call_count == 1


def test_parse_credit_agricole(mocker):
    with open('app/tests/file_html/credit_agricole.txt', 'r') as file:
        value = file.read()
    request_get_mock = mocker.patch('requests.get', return_value=MagicMock(text=value))

    # first request
    rate_initial_count = Rate.objects.count()
    parse_credit_agricole()
    assert Rate.objects.count() == rate_initial_count + 2
    assert request_get_mock.call_count == 1

    # request with no changes
    parse_credit_agricole()
    assert Rate.objects.count() == rate_initial_count + 2
    assert request_get_mock.call_count == 2
    assert request_get_mock.call_args[0] == ('https://credit-agricole.ua/kurs-valyut',)
    assert request_get_mock.call_args[1] == {}

    # request with changes
    with open('app/tests/file_html/credit_agricole2.txt', 'r') as file:
        value = file.read()
    request_get_mock_2 = mocker.patch('requests.get', return_value=MagicMock(text=value))

    assert request_get_mock_2.call_count == 0
    parse_credit_agricole()
    assert Rate.objects.count() == rate_initial_count + 3
    assert request_get_mock_2.call_count == 1


def test_parse_minfin_avarage(mocker):
    with open('app/tests/file_html/minfin_avarage.txt', 'r') as file:
        value = file.read()
    request_get_mock = mocker.patch('requests.get', return_value=MagicMock(text=value))

    # first request
    rate_initial_count = Rate.objects.count()
    parse_minfin_avarage()
    assert Rate.objects.count() == rate_initial_count + 2
    assert request_get_mock.call_count == 1

    # request with no changes
    parse_minfin_avarage()
    assert Rate.objects.count() == rate_initial_count + 2
    assert request_get_mock.call_count == 2
    assert request_get_mock.call_args[0] == ('https://minfin.com.ua/currency/banks/',)
    assert request_get_mock.call_args[1] == {}

    # request with changes
    with open('app/tests/file_html/minfin_avarage2.txt', 'r') as file:
        value = file.read()
    request_get_mock_2 = mocker.patch('requests.get', return_value=MagicMock(text=value))

    assert request_get_mock_2.call_count == 0
    parse_minfin_avarage()
    assert Rate.objects.count() == rate_initial_count + 2
    assert request_get_mock_2.call_count == 1
