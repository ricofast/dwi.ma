from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CreditWallet
from .services import grant_free_credits


@receiver(post_save, sender=get_user_model())
def create_wallet_for_new_user(sender, instance, created, **kwargs):
    if not created:
        return
    CreditWallet.objects.get_or_create(user=instance)
    grant_free_credits(instance)
