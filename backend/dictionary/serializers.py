from rest_framework.serializers import ModelSerializer
from .models import Dictionary, Enwords, Ruwords, Categories, Profile, Ratings, UserDictionaries


class RatingsSerializer(ModelSerializer):
    class Meta:
        model = Ratings
        fields = ["name"]


class ProfileSerializer(ModelSerializer):
    rating = RatingsSerializer()

    class Meta:
        model = Profile
        fields = ['name', 'count_words', 'rating']

    def create(self, validated_data):
        return Profile(**validated_data)


class EnwordsSerializer(ModelSerializer):
    class Meta:
        model = Enwords
        fields = ["word"]


class RuwordsSerializer(ModelSerializer):
    class Meta:
        model = Ruwords
        fields = ["word"]


class CategoriesSerializer(ModelSerializer):
    class Meta:
        model = Categories
        fields = ("name",)


class DictionarySerializer(ModelSerializer):
    en_word = EnwordsSerializer()
    ru_word = RuwordsSerializer()
    category = CategoriesSerializer()

    class Meta:
        model = Dictionary
        fields = ['en_word', 'ru_word', 'category']

    def create(self, validated_data):
        return Dictionary(**validated_data)


class UserDictionariesSerializer(ModelSerializer):

    class Meta:
        model = UserDictionaries
        fields = '__all__'

    def create(self, validated_data):
        return UserDictionaries(**validated_data)
