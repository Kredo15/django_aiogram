from django.db.models import Subquery
from .. import models
from ..serializers import DictionarySerializer, \
    UserDictionariesSerializer


def get_word_for_study(user: int = None,
                       name_category: str = None,
                       pk: int = 0
                       ) -> dict:
    words_in_learn = models.UserDictionaries.objects.filter(user__username=user)
    if words_in_learn:
        word = models.Dictionary.objects.filter(pk__gt=pk,
                                                category__name=name_category.capitalize()).\
            exclude(id__in=Subquery(words_in_learn.values('word'))).first()
    else:
        word = models.Dictionary.objects.select_related(
            'en_word', 'ru_word', 'category'
        ).filter(pk__gt=pk).first()
    serialize_in_learn = DictionarySerializer(word)
    return serialize_in_learn.data


def add_word_for_study(data: dict = None) -> tuple[bool, dict]:
    serializer_new_word = DictionarySerializer(data=data, many=True)
    if serializer_new_word.is_valid():
        serializer_new_word.save()
        return True, serializer_new_word.data
    return False, serializer_new_word.errors


def get_studied_word(user: int = None,
                     is_learn: bool = False
                     ) -> dict:
    words = models.UserDictionaries.objects.filter(
        user__username=user, is_learn=is_learn
    ).all()[:5]
    return UserDictionariesSerializer(words).data


def add_word_studied(data: dict = None) -> tuple[bool, dict]:
    serializer_word_studied = UserDictionariesSerializer(data=data, many=True)
    if serializer_word_studied.is_valid():
        serializer_word_studied.save()
        return True, serializer_word_studied.data
    return False, serializer_word_studied.errors


def update_word_studied(data: dict = None) -> tuple[bool, dict]:
    instance = models.UserDictionaries.objects.get(user__username=data.get("user"),
                                                   word=data.get("word"))
    serializer_word_studied = UserDictionariesSerializer(data=data, instance=instance)
    if serializer_word_studied.is_valid():
        serializer_word_studied.save()
        return True, serializer_word_studied.data
    return False, serializer_word_studied.errors


def add_number_words_studied(username: str, counter: int):
    instance = models.Profile.objects.get(user=username)
    instance.number_half_learned_words -= counter
    instance.number_words_studied += 1
    instance.save()


def add_number_half_learned_words(username: str):
    instance = models.Profile.objects.get(user=username)
    instance.number_half_learned_words += 1
    instance.save()
