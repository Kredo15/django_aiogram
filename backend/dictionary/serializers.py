from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import Dictionary, Enwords, Ruwords, \
    Categories, Profile, Ratings, UserDictionaries


class RatingsSerializer(ModelSerializer):
    class Meta:
        model = Ratings
        fields = ["name"]

    def create(self, validated_data):
        return Ratings(**validated_data)


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name']

    def create(self, validated_data):
        return User(**validated_data)


class ProfileSerializer(ModelSerializer):
    user = UserSerializer()
    rating = RatingsSerializer()

    class Meta:
        model = Profile
        fields = ['user', 'count_words', 'rating']

    def create(self, validated_data):
        user_data = User.objects.create_user(
            username=validated_data.get("name"))
        post = Profile(user=user_data)
        return post

    def update(self, instance, validated_data):
        instance.user = validated_data.get("name", instance.user)
        instance.count = UserDictionaries.objects.filter(
            is_learn=True).count()
        instance.rating = Ratings.objects.filter(
            criteria__lte=instance.count).order_by("criteria").reverse().first()
        instance.save()
        return instance


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
        post = Dictionary.objects.create(
            en_word=en_word_data,
            ru_word=ru_word_data,
            category=category_data)
        return post


class UserDictionariesSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserDictionaries
        fields = '__all__'
        exclude = ['id', 'is_learn']

    def create(self, validated_data):
        user_data = User.objects.get_by_natural_key(
            username=validated_data.get("name"))
        word_data = Dictionary.objects.get(
            pk=validated_data.get("pk"))
        post = UserDictionaries(
            user=user_data,
            word=word_data
        )
        return post

    def update(self, instance, validated_data):
        instance.translate_choose_ru = validated_data.get(
            "translate_choose_ru", instance.translate_choose_ru
        )
        instance.translate_choose_en = validated_data.get(
            "translate_choose_en", instance.translate_choose_en
        )
        instance.translate_write_ru = validated_data.get(
            "translate_write_ru", instance.translate_write_ru
        )
        instance.translate_write_en = validated_data.get(
            "translate_write_en", instance.translate_write_en
        )
        instance.write_word_using_audio = validated_data.get(
            "write_word_using_audio", instance.write_word_using_audio
        )
        instance.save()
        return instance
