import logging
from datetime import datetime

from django.contrib.auth.models import User
from .. import models
from ..serializers import ProfileSerializer

logger = logging.getLogger(__name__)


def get_user_data(user: int = None) -> dict:
    try:
        user_data = models.Profile.objects.get(user__username=user)
        return ProfileSerializer(user_data).data
    except models.Profile.DoesNotExist as e:
        logger.error(f'{user} get_user_data: {e}')
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


def get_users_for_activity():
    now = datetime.now()
    users_for_activity = User.objects.filter(date_joined__lt=now)
    return ProfileSerializer(users_for_activity, many=True).data
