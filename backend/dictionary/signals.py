from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import UserDictionaries
from .services.dictionary import add_number_words_studied, \
    add_number_half_learned_words


@receiver(pre_save, sender=UserDictionaries)
def update_studied_step_word(sender, instance, **kwargs):
    result = []
    for field in instance._meta.get_fields():
        if field.name not in ('id', 'user', 'word', 'is_learn'):
            result.append(getattr(instance, field.name))
    if all(result):
        instance.is_learn = True
    return instance


@receiver(post_save, sender=UserDictionaries)
def update_number_word_studied(sender, instance, created, **kwargs):
    if created:
        counter = 0
    else:
        counter = 1
    if instance.is_learn:
        add_number_words_studied(instance.user, counter)
    else:
        add_number_half_learned_words(instance.user)
