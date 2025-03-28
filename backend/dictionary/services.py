from django.db.models import Subquery
from . import models
from rest_framework.serializers import ModelSerializer
from .serializers import DictionarySerializer, ProfileSerializer, UserDictionariesSerializer


def get_user_data(user: int = None) -> str:
    data_user = models.Profile.objects.filter(user=user).values('name', 'count_words', 'rating')
    return ProfileSerializer(data_user, many=True).data


def add_user_data(data: str = None) -> tuple[bool, str]:
    serializer_data_user: ModelSerializer = ProfileSerializer(data=data)
    if serializer_data_user.is_valid():
        serializer_data_user.save()
        return True, serializer_data_user.data
    return False, serializer_data_user.errors


def get_word_for_study(user: int = None, name_category: str = None) -> str:
    words_in_learn = models.UserDictionaries.objects.filter(user=user)
    if words_in_learn:
        word = models.Dictionary.objects.annotate(word=Subquery(words_in_learn)).filter(
            category__name=name_category).values('en_word', 'ru_word', 'category').first()
    else:
        word = models.Dictionary.objects.select_related('en_word', 'ru_word', 'category').all()[:1]
    return DictionarySerializer(word, many=True).data


def add_word_for_study(data: str = None) -> tuple[bool, str]:
    serializer_new_word: ModelSerializer = DictionarySerializer(data=data)
    if serializer_new_word.is_valid():
        serializer_new_word.save()
        return True, serializer_new_word.data
    return False, serializer_new_word.errors


def get_repetition_word(user: int = None, is_learn: bool = False) -> str:
    words = models.UserDictionaries.objects.filter(user=user, is_learn=is_learn).all()[:10]
    return UserDictionariesSerializer(words, many=True).data


def add_word_studied(data: str = None) -> tuple[bool, str]:
    serializer_word_studied: ModelSerializer = UserDictionariesSerializer(data=data)
    if serializer_word_studied.is_valid():
        serializer_word_studied.save()
        return True, serializer_word_studied.data
    return False, serializer_word_studied.errors
