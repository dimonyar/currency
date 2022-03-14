from django.db import models


class ContactUs(models.Model):
    email_from = models.EmailField(max_length=254)
    subject = models.CharField(max_length=200)
    message = models.TextField(max_length=1000)


class Rate(models.Model):
    type = models.CharField(max_length=5)  # noqa: VNE003, A003
    source = models.CharField(max_length=64)
    created = models.DateTimeField()
    buy = models.DecimalField(max_digits=10, decimal_places=2)
    sale = models.DecimalField(max_digits=10, decimal_places=2)
