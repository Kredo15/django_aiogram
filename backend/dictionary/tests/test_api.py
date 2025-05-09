from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from ..models import Ratings, Categories, Dictionary, Enwords, Ruwords, Profile, UserDictionaries
from django.contrib.auth.models import User
from ..serializers import RatingsSerializer, CategoriesSerializer, DictionarySerializer, ProfileSerializer, \
    UserDictionariesSerializer


class RatingsApiTestCase(APITestCase):

    def test_get(self):
        rating_1 = Ratings.objects.create(name='Test rating 1', criteria=10)
        rating_2 = Ratings.objects.create(name='Test rating 2', criteria=30)
        url = reverse("ratings")
        response = self.client.get(url, format='list')
        serializer_data = RatingsSerializer([rating_1, rating_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data, serializer_data)


class CategoriesApiTextCase(APITestCase):

    def test_get(self):
        category_1 = Categories.objects.create(name='Test category 1')
        category_2 = Categories.objects.create(name='Test category 2')
        url = reverse('categories')
        response = self.client.get(url, format='list')
        serializer_data = CategoriesSerializer([category_1, category_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data, serializer_data)


class NewWordApiTextCase(APITestCase):

    def test_get(self):
        en_word_data_1 = Enwords.objects.create(word='Test en_word 1')
        ru_word_data_1 = Ruwords.objects.create(word='Test ru_word 1')
        category_data_1 = Categories.objects.create(name='Test category 1')
        dictionary_1 = Dictionary.objects.create(en_word=en_word_data_1,
                                                 ru_word=ru_word_data_1,
                                                 category=category_data_1)
        kwargs = {
            'user': 'test user',
            'name_category': 'Test category 1',
            'pk': 0
        }
        url = reverse('new_word')
        qs = '&'.join([f'{key}={value}' for key, value in kwargs.items()])
        url_get = '?'.join((url, qs))
        response = self.client.get(url_get)
        serializer_data = DictionarySerializer(dictionary_1).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data, serializer_data)


class UserApiTextCase(APITestCase):

    def test_get(self):
        user_data = User.objects.create_user(username="Test user")
        rating_data = Ratings.objects.create(name='Test rating 1', criteria=10)
        profile = Profile.objects.create(user=user_data, rating=rating_data)
        url = reverse('user')
        kwargs = {
            'user': "Test user"
        }
        qs = '&'.join([f'{key}={value}' for key, value in kwargs.items()])
        url_get = '?'.join((url, qs))
        response = self.client.get(url_get)
        serializer_data = ProfileSerializer(profile).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data, serializer_data)


class StudiedWordApiTextCase(APITestCase):

    def test_get(self):
        en_word_data_1 = Enwords.objects.create(word='Test en_word 1')
        ru_word_data_1 = Ruwords.objects.create(word='Test ru_word 1')
        category_data_1 = Categories.objects.create(name='Test category 1')
        dictionary_1 = Dictionary.objects.create(en_word=en_word_data_1,
                                                 ru_word=ru_word_data_1,
                                                 category=category_data_1)
        en_word_data_2 = Enwords.objects.create(word='Test en_word 2')
        ru_word_data_2 = Ruwords.objects.create(word='Test ru_word 2')
        dictionary_2 = Dictionary.objects.create(en_word=en_word_data_2,
                                                 ru_word=ru_word_data_2,
                                                 category=category_data_1)
        user_data = User.objects.create_user(username="Test user")
        rating_data = Ratings.objects.create(name='Test rating 1', criteria=10)
        profile = Profile.objects.create(user=user_data, rating=rating_data)
        user_dictionary_1 = UserDictionaries.objects.create(user=user_data,
                                                            word=dictionary_1)
        user_dictionary_2 = UserDictionaries.objects.create(user=user_data,
                                                            word=dictionary_2)
        kwargs = {
            'user': "Test user"
        }
        url = reverse('studied_word')
        qs = '&'.join([f'{key}={value}' for key, value in kwargs.items()])
        url_get = '?'.join((url, qs))
        response = self.client.get(url_get)
        serializer_data = UserDictionariesSerializer([user_dictionary_1, user_dictionary_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data, serializer_data)
