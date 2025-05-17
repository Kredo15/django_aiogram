from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views


urlpatterns = [
    path('ratings/', views.RatingsData.as_view(), name="ratings"),
    path('categories/', views.CategoriesData.as_view(), name="categories"),
    path('new_word/', views.WordForStudy.as_view(), name="new_word"),
    path('user/', views.UserData.as_view(), name="user"),
    path('users_for_activity/', views.UsersForActivity.as_view(), name="users_for_activity"),
    path('studied_word/', views.WordFromUserDictionary.as_view(), name="studied_word"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
