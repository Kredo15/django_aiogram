from .. import models
from ..serializers import ProfileSerializer


def get_user_data(user: int = None) -> dict:
    try:
        user_data = models.Profile.objects.get(user__username=user)
        return ProfileSerializer(user_data).data
    except models.Profile.DoesNotExist:
        return {}


def add_user_data(data: dict = None) -> tuple[bool, dict]:
    data["rating"] = {"name": "новичок"}
    serializer_data_user = ProfileSerializer(data=data)
    if serializer_data_user.is_valid():
        serializer_data_user.save()
        return True, serializer_data_user.data
    return False, serializer_data_user.errors


def update_user_data(data: dict = None) -> tuple[bool, dict]:
    instance = models.Profile.objects.get(user=data.get("user"))
    serializer_data_user = ProfileSerializer(data=data, instance=instance)
    if serializer_data_user.is_valid():
        return True, serializer_data_user.data
    return False, serializer_data_user.errors

