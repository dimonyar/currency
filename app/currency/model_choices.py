from django.db import models


class RateType(models.TextChoices):
    USD = 'USD', 'Dollar'
    EUR = 'EUR', 'Euro'
    BTC = 'BTC', 'Bitcoin'
    UAH = 'UAH', 'Hryvnia'


class SourceCodeName(models.IntegerChoices):
    PRIVATBANK = 1, 'PrivatBank'
    MONOBANK = 2, 'MonoBank'
    VKURSE = 3, 'vkurse.dp.ua'

