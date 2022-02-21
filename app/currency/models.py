from django.db import models


class ContactUs(models.Model):
    email_from = models.EmailField(max_length=254)
    subject = models.CharField(max_length=200)
    message = models.TextField(max_length=1000)

