from django.test import TestCase

from ..models import Ratings, Categories, Dictionary, Enwords, Ruwords, Profile, UserDictionaries
from django.contrib.auth.models import User
from ..serializers import RatingsSerializer, CategoriesSerializer, DictionarySerializer, ProfileSerializer, \
    UserDictionariesSerializer


class RatingsSerializerTestCase(TestCase):

    def test_valid_rating_serializer(self):
        rating_1 = Ratings.objects.create(name='Test rating 1', criteria=10)
        rating_2 = Ratings.objects.create(name='Test rating 2', criteria=30)
        data = RatingsSerializer([rating_1, rating_2], many=True).data
        excepted_data = [
            {
                'name': 'Test rating 1',
                'criteria': 10
            },
            {
                'name': 'Test rating 2',
                'criteria': 30
            }
        ]
        self.assertEqual(excepted_data, data)


class CategoriesSerializerTestCase(TestCase):

    def test_valid_categories_serializer(self):
        category_1 = Categories.objects.create(name='Test category 1')
        category_2 = Categories.objects.create(name='Test category 2')
        data = CategoriesSerializer([category_1, category_2], many=True).data
        excepted_data = [
            {
                'name': 'Test category 1'
            },
            {
                'name': 'Test category 2'
            }
        ]
        self.assertEqual(excepted_data, data)


class DictionarySerializerTestCase(TestCase):

    def test_valid_dictionary_serializer(self):
        en_word_data_1 = Enwords.objects.create(word='Test en_word 1')
        ru_word_data_1 = Ruwords.objects.create(word='Test ru_word 1')
        category_data_1 = Categories.objects.create(name='Test category 1')
        dictionary_1 = Dictionary.objects.create(en_word=en_word_data_1,
                                                 ru_word=ru_word_data_1,
                                                 category=category_data_1)
        en_word_data_2 = Enwords.objects.create(word='Test en_word 2')
        ru_word_data_2 = Ruwords.objects.create(word='Test ru_word 2')
        category_data_2 = Categories.objects.create(name='Test category 2')
        dictionary_2 = Dictionary.objects.create(en_word=en_word_data_2,
                                                 ru_word=ru_word_data_2,
                                                 category=category_data_2)
        data = DictionarySerializer([dictionary_1, dictionary_2], many=True).data
        excepted_data = [
            {
                'id': dictionary_1.id,
                'en_word': {
                    'word': 'Test en_word 1'
                },
                'ru_word': {
                    'word': 'Test ru_word 1'
                },
                'category': {
                    'name': 'Test category 1'
                }

            },
            {
                'id': dictionary_2.id,
                'en_word': {
                    'word': 'Test en_word 2'
                },
                'ru_word': {
                    'word': 'Test ru_word 2'
                },
                'category': {
                    'name': 'Test category 2'
                }

            }
        ]
        self.assertEqual(excepted_data, data)


class ProfileSerializerTestCase(TestCase):

    def test_valid_profile_serializer(self):
        user_data = User.objects.create_user(username="Test user")
        rating_data = Ratings.objects.create(name='Test rating 1', criteria=10)
        profile = Profile.objects.create(user=user_data, rating=rating_data)
        data = ProfileSerializer(profile).data
        excepted_data = {
                'user': {
                    'username': 'Test user'
                },
                'number_words_studied': 0,
                'number_half_learned_words': 0,
                'rating': {
                    'name': 'Test rating 1',
                    'criteria': 10
                }
            }
        self.assertEqual(excepted_data, data)


class UserDictionariesSerializerTestCase(TestCase):

    def test_valid_user_dictionary_serializer(self):
        en_word_data_1 = Enwords.objects.create(word='Test en_word 1')
        ru_word_data_1 = Ruwords.objects.create(word='Test ru_word 1')
        category_data_1 = Categories.objects.create(name='Test category 1')
        dictionary = Dictionary.objects.create(en_word=en_word_data_1,
                                               ru_word=ru_word_data_1,
                                               category=category_data_1)
        user_data = User.objects.create_user(username="Test user")
        rating_data = Ratings.objects.create(name='Test rating 1', criteria=10)
        profile = Profile.objects.create(user=user_data, rating=rating_data)
        user_dictionary = UserDictionaries.objects.create(user=user_data,
                                                          word=dictionary)
        data = UserDictionariesSerializer(user_dictionary).data
        excepted_data = {
            'user': "Test user",
            'word': dictionary.id,
            'translate_choose_ru': False,
            'translate_choose_en': False,
            'translate_write_ru': False,
            'translate_write_en': False,
            'write_word_using_audio': False
            }
        self.assertEqual(excepted_data, data)
