from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('new_word/', views.WordForStudy.as_view()),
    path('user/', views.DataUser.as_view()),
    path('repetition/', views.RepetitionWord.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
