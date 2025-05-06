from django.test import TestCase

from ..models import Ratings, Categories, Dictionary, Enwords, Ruwords
from ..serializers import RatingsSerializer, CategoriesSerializer, DictionarySerializer


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

    def test_valid_rating_serializer(self):
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

    def test_valid_rating_serializer(self):
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
