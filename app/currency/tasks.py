from decimal import Decimal

from bs4 import BeautifulSoup

from celery import shared_task

from currency import model_choices as mch
from currency.models import Rate, Source

from django.core.mail import send_mail

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
        currency_type = available_currencies.get(rate['ccy'])

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


@shared_task
def parse_oschadbank():
    url = 'https://www.oschadbank.ua/currency-rate'
    response = requests.get(url)
    response.raise_for_status()
    src = response.text
    available_currencies = {
        'USD': mch.RateType.USD,
        'EUR': mch.RateType.EUR,
    }

    base_currency_type = mch.RateType.UAH

    try:
        source = Source.objects.get(code_name=mch.SourceCodeName.OSCHADBANK)
    except Source.DoesNotExist:
        source = Source.objects.create(code_name=mch.SourceCodeName.OSCHADBANK, name='OschadBank', url=url)

    soup = BeautifulSoup(src, "lxml")

    header_currency = soup.find("div", class_="currency header__currency").find_all("div", class_="currency__item")

    for div in header_currency:
        item_name = div.find("span", class_="currency__item_name").string
        if item_name not in available_currencies:
            continue
        currency_type = available_currencies.get(item_name)

        if not currency_type:
            continue

        values = div.find_all("span", class_="currency__item_value")

        sale = round_decimal(values[1].text)
        buy = round_decimal(values[0].text)

        last_rate = Rate.objects.filter(source=source, type=currency_type) \
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
def parse_credit_agricole():
    url = 'https://credit-agricole.ua/kurs-valyut'
    response = requests.get(url)
    response.raise_for_status()
    src = response.text
    available_currencies = {
        'USD': mch.RateType.USD,
        'EUR': mch.RateType.EUR,
    }

    base_currency_type = mch.RateType.UAH

    try:
        source = Source.objects.get(code_name=mch.SourceCodeName.CREDIT_AGRICOLE)
    except Source.DoesNotExist:
        source = Source.objects.create(code_name=mch.SourceCodeName.CREDIT_AGRICOLE,
                                       name='Credit-Agricole', url=url)

    soup = BeautifulSoup(src, "lxml")
    table_content = soup.find("div", class_="exchange-rates-table")
    currency_list = table_content.find_all("div", class_="currency")

    for item_div in currency_list:
        div_list = item_div.find_all("div")
        if div_list[0].text not in available_currencies:
            continue
        currency_type = available_currencies.get(div_list[0].text)

        if not currency_type:
            continue

        sale = round_decimal(div_list[2].text.strip())
        buy = round_decimal(div_list[1].text.strip())

        last_rate = Rate.objects.filter(source=source, type=currency_type) \
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
def parse_minfin_avarage():
    """
    Average rate for banks from the site minfin.com.ua
    """
    url = 'https://minfin.com.ua/currency/banks/'
    response = requests.get(url)
    response.raise_for_status()
    src = response.text
    available_currencies = {
        'ДОЛЛАР': mch.RateType.USD,
        'ЕВРО': mch.RateType.EUR,
    }

    base_currency_type = mch.RateType.UAH

    try:
        source = Source.objects.get(code_name=mch.SourceCodeName.MINFIN)
    except Source.DoesNotExist:
        source = Source.objects.create(code_name=mch.SourceCodeName.MINFIN,
                                       name='MinFin Avarage', url=url)

    soup = BeautifulSoup(src, "lxml")

    table_content = soup.find("table", class_="table-response mfm-table mfcur-table-lg-banks mfcur-table-lg")
    currency_list = table_content.find_next().find_next_sibling().find_all("tr")

    for td_item in currency_list:
        td_name = td_item.find("td", class_="mfcur-table-cur").text.strip()
        if td_name not in available_currencies:
            continue
        currency_type = available_currencies.get(td_name)

        values = td_item.find("td", class_="mfm-text-nowrap").text.strip()

        sale = round_decimal(values[-6:])
        buy = round_decimal(values[:6])

        last_rate = Rate.objects.filter(source=source, type=currency_type) \
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
def sendmail_new_сontactus(subject: str, message_body: str, from_email: str):
    send_mail(
        subject,
        message_body,
        from_email,
        ['d.yaroshevsky@gmail.com'],
        fail_silently=False,
    )
