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

        sale = round_decimal(rate["sale"])
        buy = round_decimal(rate['buy'])

        last_rate = Rate.objects.filter(source=source, type=currency_type).order_by('-created').first()

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
