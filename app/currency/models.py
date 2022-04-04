from currency import model_choices as mch

from django.db import models


class ContactUs(models.Model):
    email_from = models.EmailField(max_length=254)
    subject = models.CharField(max_length=200)
    message = models.TextField(max_length=1000)


class Rate(models.Model):
    type = models.CharField(max_length=5, choices=mch.RateType.choices)  # noqa: VNE003, A003
    source = models.CharField(max_length=64)
    created = models.DateTimeField()
    buy = models.DecimalField(max_digits=10, decimal_places=2)
    sale = models.DecimalField(max_digits=10, decimal_places=2)


class Source(models.Model):
    name = models.CharField(max_length=64)
    source_url = models.CharField(max_length=255)
    fitch_ratings = models.CharField(max_length=10, null=True, blank=True)
    social_items = models.CharField(max_length=255, null=True, blank=True)
