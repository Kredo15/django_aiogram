from django.urls import path
from . import views


urlpatterns = [
    path('ratings/', views.RatingsData.as_view(), name="ratings"),
    path('categories/', views.CategoriesData.as_view(), name="categories"),
    path('new_word/', views.WordForStudy.as_view(), name="new_word"),
    path('user/', views.UserData.as_view(), name="user"),
    path('studied_word/', views.WordFromUserDictionary.as_view(), name="studied_word")
]
