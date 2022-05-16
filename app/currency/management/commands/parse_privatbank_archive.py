from datetime import datetime, timedelta

from currency import model_choices as mch
from currency.models import Rate, Source
from currency.tasks import round_decimal

from django.core.management.base import BaseCommand

import requests


class Command(BaseCommand):
    help = 'Parse Privatbank archive rates' # noqa VNE003, A003

    def handle(self, *args, **options):
        base_url = 'https://api.privatbank.ua/p24api/exchange_rates'

        end_date = datetime.now()
        start_date = datetime.now() - timedelta(days=365 * 4)
        total_days = (end_date - start_date).days

        available_currencies = {
            'USD': mch.RateType.USD,
            'EUR': mch.RateType.EUR,
            'UAH': mch.RateType.UAH,
        }

        try:
            source = Source.objects.get(code_name=mch.SourceCodeName.PRIVATBANK)
        except Source.DoesNotExist:
            source = Source.objects.create(code_name=mch.SourceCodeName.PRIVATBANK, name='PrivatBank', url=base_url)

        for day in range(total_days):
            current_day = start_date + timedelta(days=day)
            params = {
                'json': '',
                'date': current_day.strftime("%d.%m.%Y"),
            }

            response = requests.get(base_url, params=params)
            response.raise_for_status()
            rates = response.json()

            for rate in rates["exchangeRate"]:
                if len(rate) < 6:
                    continue
                if 'currency' not in rate or rate['currency'] not in available_currencies:
                    continue
                currency_type = available_currencies.get(rate['currency'])

                if not currency_type:
                    continue

                base_currency_type = available_currencies.get(rate['baseCurrency'])

                sale = round_decimal(rate['saleRate'])
                buy = round_decimal(rate['purchaseRate'])

                if Rate.objects.get(source=source,
                                    type=currency_type,
                                    base_type=base_currency_type,
                                    sale=sale,
                                    buy=buy,
                                    created__date=current_day
                                    ):
                    continue

                Rate.objects.create(
                    type=currency_type,
                    base_type=base_currency_type,
                    sale=sale, buy=buy,
                    source=source,
                    created=current_day
                )
