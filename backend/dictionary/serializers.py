from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import Dictionary, Enwords, Ruwords, \
    Categories, Profile, Ratings, UserDictionaries


class RatingsSerializer(ModelSerializer):
    class Meta:
        model = Ratings
        fields = ["name", "criteria"]

    def create(self, validated_data):
        return Ratings.objects.create(**validated_data)


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name']

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class ProfileSerializer(ModelSerializer):
    user = UserSerializer()
    rating = RatingsSerializer()

    class Meta:
        model = Profile
        fields = ['user', 'count_words', 'rating']

    def create(self, validated_data):
        user_data = User.objects.create_user(
            username=validated_data.get("user").get("username"),
            first_name=validated_data.get("user").get("first_name"))
        rating_data = Ratings.objects.get(name=validated_data.get("rating").get("name"))
        post = Profile.objects.create(user=user_data, rating=rating_data)
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
        return Enwords.objects.create(**validated_data)


class RuwordsSerializer(ModelSerializer):
    class Meta:
        model = Ruwords
        fields = ["word"]

    def create(self, validated_data):
        return Ruwords.objects.create(**validated_data)


class CategoriesSerializer(ModelSerializer):
    class Meta:
        model = Categories
        fields = ["name"]

    def create(self, validated_data):
        return Categories.objects.create(**validated_data)


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
        for key, value in validated_data:
            setattr(instance, key, value)
        instance.save()
        return instance
