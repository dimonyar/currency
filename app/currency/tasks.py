from decimal import Decimal

from celery import shared_task

from currency import model_choices as mch
from currency.models import Rate, Source

import requests


def round_decimal(value: str) -> Decimal:
    places = Decimal(10) ** -2
    return Decimal(value).quantize(places)


@shared_task
def parse_privatbank():
    url = 'https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11'
    response = requests.get(url)
    response.raise_for_status()
    rates = response.json()
    available_currencies = {
        'USD': mch.RateType.USD,
        'EUR': mch.RateType.EUR,
        'BTC': mch.RateType.BTC,
        'UAH': mch.RateType.UAH,
    }

    try:
        source = Source.objects.get(code_name=mch.SourceCodeName.PRIVATBANK)
    except Source.DoesNotExist:
        source = Source.objects.create(code_name=mch.SourceCodeName.PRIVATBANK, name='PrivatBank', url=url)

    for rate in rates:
        if rate['ccy'] not in available_currencies:
            continue
        currency_type = rate['ccy']

        if not currency_type:
            continue

        base_currency_type = available_currencies.get(rate['base_ccy'])

        sale = round_decimal(rate['sale'])
        buy = round_decimal(rate['buy'])

        last_rate = Rate.objects.filter(source=source, type=currency_type, base_type=base_currency_type) \
            .order_by('-created').first()

        if (last_rate is None or  # does not exist in table
                last_rate.sale != sale or
                last_rate.buy != buy):
            Rate.objects.create(
                type=currency_type,
                base_type=base_currency_type,
                sale=sale,
                buy=buy,
                source=source,
            )


@shared_task
def parse_monobank():
    url = 'https://api.monobank.ua/bank/currency'
    response = requests.get(url)
    response.raise_for_status()
    rates = response.json()
    available_currencies = {
        840: mch.RateType.USD,
        978: mch.RateType.EUR,
        980: mch.RateType.UAH,
    }

    try:
        source = Source.objects.get(code_name=mch.SourceCodeName.MONOBANK)
    except Source.DoesNotExist:
        source = Source.objects.create(code_name=mch.SourceCodeName.MONOBANK, name='MonoBank', url=url)

    for rate in rates:
        if rate['currencyCodeA'] not in available_currencies:
            continue
        currency_type = available_currencies.get(rate['currencyCodeA'])

        if not currency_type:
            continue

        base_currency_type = available_currencies.get(rate['currencyCodeB'])

        sale = round_decimal(rate['rateSell'])
        buy = round_decimal(rate['rateBuy'])

        last_rate = Rate.objects.filter(source=source, type=currency_type, base_type=base_currency_type) \
            .order_by('-created').first()

        if (last_rate is None or
                last_rate.sale != sale or
                last_rate.buy != buy):
            Rate.objects.create(
                type=currency_type,
                base_type=base_currency_type,
                sale=sale,
                buy=buy,
                source=source,
            )


@shared_task
def parse_vkurse():
    url = 'http://www.vkurse.dp.ua/course.json'
    response = requests.get(url)
    response.raise_for_status()
    rates = response.json()
    available_currencies = {
        'Dollar': mch.RateType.USD,
        'Euro': mch.RateType.EUR,
    }

    try:
        source = Source.objects.get(code_name=mch.SourceCodeName.VKURSE)
    except Source.DoesNotExist:
        source = Source.objects.create(code_name=mch.SourceCodeName.VKURSE, name='vkurse.dp.ua', url=url)

    base_currency_type = mch.RateType.UAH

    for rate in rates.keys():
        if rate not in available_currencies:
            continue
        currency_type = available_currencies.get(rate)

        if not currency_type:
            continue

        value = rates[rate]

        sale = round_decimal(value['sale'])
        buy = round_decimal(value['buy'])

        last_rate = Rate.objects.filter(source=source, type=currency_type).order_by('-created').first()

        if (last_rate is None or
                last_rate.sale != sale or
                last_rate.buy != buy):
            Rate.objects.create(
                type=currency_type,
                base_type=base_currency_type,
                sale=sale,
                buy=buy,
                source=source,
            )
