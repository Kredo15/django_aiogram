from rest_framework.serializers import ModelSerializer
from .models import Dictionary, Enwords, Ruwords, Categories, Profile, Ratings, UserDictionaries


class RatingsSerializer(ModelSerializer):
    class Meta:
        model = Ratings
        fields = ["name"]

    def create(self, validated_data):
        return Ratings(**validated_data)


class ProfileSerializer(ModelSerializer):
    rating = RatingsSerializer()

    class Meta:
        model = Profile
        fields = ['name', 'count_words', 'rating']

    def create(self, validated_data):
        rating_data, _ = Ratings.objects.get_or_create(
            name=validated_data.get("rating").get("name"))
        post = Profile(name=validated_data.get("name"),
                       count_words=validated_data.get("count_words"),
                       rating=rating_data)
        return post


class EnwordsSerializer(ModelSerializer):
    class Meta:
        model = Enwords
        fields = ["word"]

    def create(self, validated_data):
        return Enwords(**validated_data)


class RuwordsSerializer(ModelSerializer):
    class Meta:
        model = Ruwords
        fields = ["word"]

    def create(self, validated_data):
        return Ruwords(**validated_data)


class CategoriesSerializer(ModelSerializer):
    class Meta:
        model = Categories
        fields = ["name"]

    def create(self, validated_data):
        return Categories(**validated_data)


class DictionarySerializer(ModelSerializer):
    en_word = EnwordsSerializer()
    ru_word = RuwordsSerializer()
    category = CategoriesSerializer()

    class Meta:
        model = Dictionary
        fields = '__all__'

    def create(self, validated_data):
        en_word_data, _ = Enwords.objects.get_or_create(
            word=validated_data.get("en_word").get("word"))
        ru_word_data, _ = Ruwords.objects.get_or_create(
            word=validated_data.get("ru_word").get("word"))
        category_data, _ = Categories.objects.get_or_create(
            name=validated_data.get("category").get("name"))
        post = Dictionary.objects.create(en_word=en_word_data,
                                         ru_word=ru_word_data,
                                         category=category_data)
        return post


class UserDictionariesSerializer(ModelSerializer):
    class Meta:
        model = UserDictionaries
        fields = '__all__'

    def create(self, validated_data):
        return UserDictionaries(**validated_data)
