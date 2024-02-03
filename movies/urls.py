from django.urls import path
from .views import RegisterUser, MovieList
urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('movies/', MovieList.as_view(), name='movies'),
]