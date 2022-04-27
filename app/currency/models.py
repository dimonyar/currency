from currency import model_choices as mch

from django.db import models
from django.templatetags.static import static


class ContactUs(models.Model):
    email_from = models.EmailField(max_length=254)
    subject = models.CharField(max_length=200)
    message = models.TextField(max_length=1000)


class Source(models.Model):
    name = models.CharField(max_length=64, unique=True)
    code_name = models.PositiveSmallIntegerField(choices=mch.SourceCodeName.choices, unique=True)
    url = models.CharField(max_length=255)
    social = models.CharField(max_length=255, null=True, blank=True)
    logo = models.FileField(upload_to='bank_logo', default=None, null=True, blank=True)

    def __str__(self):
        return self.name

    def logo_url(self):
        if self.logo:
            return self.logo.url

        return static('img/bank-logo.png')


class Rate(models.Model):
    type = models.CharField(max_length=5, choices=mch.RateType.choices)  # noqa: VNE003, A003
    base_type = models.CharField(max_length=5, choices=mch.RateType.choices, default=mch.RateType.UAH)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    buy = models.DecimalField(max_digits=10, decimal_places=2)
    sale = models.DecimalField(max_digits=10, decimal_places=2)
