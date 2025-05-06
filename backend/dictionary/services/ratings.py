from .. import models
from ..serializers import RatingsSerializer


def get_all_ratings() -> dict:
    ratings_data = models.Ratings.objects.all()
    return RatingsSerializer(ratings_data, many=True).data


def add_ratings(data: dict = None) -> tuple[bool, dict]:
    serializer_ratings = RatingsSerializer(data=data)
    if serializer_ratings.is_valid():
        serializer_ratings.save()
        return True, serializer_ratings.data
    return False, serializer_ratings.errors
