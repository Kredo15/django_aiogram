from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import UserDictionaries


@receiver(pre_save, sender=UserDictionaries)
def update_studied_step_word(sender, instance, **kwargs):
    result = []
    for field in instance._meta.get_fields():
        if field.name not in ('id', 'user', 'word', 'is_learn'):
            result.append(getattr(instance, field.name))
    if all(result):
        instance.is_learn = True
    return instance
