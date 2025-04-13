from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserDictionaries


@receiver(post_save, sender=UserDictionaries)
def update_studied_step_word(sender, instance, created, **kwargs):
    pass
