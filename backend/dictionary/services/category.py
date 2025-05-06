from .. import models
from ..serializers import CategoriesSerializer


def get_all_categories() -> dict:
    categories_data = models.Categories.objects.all()
    return CategoriesSerializer(categories_data, many=True).data


def add_category(data: dict = None) -> tuple[bool, dict]:
    serializer_category = CategoriesSerializer(data=data)
    if serializer_category.is_valid():
        serializer_category.save()
        return True, serializer_category.data
    return False, serializer_category.errors
