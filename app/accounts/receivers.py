from accounts.models import User

from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=User)
def pre_save_user_phone_change(sender, instance, **kwargs):
    if not instance.phone.isdigit():
        instance.phone = ''.join(i for i in instance.phone if i.isdigit())
