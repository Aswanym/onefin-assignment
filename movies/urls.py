from django.urls import path
from .views import (
    RegisterUser,
    MovieList,
    MovieCollection,
    LoginUser,
    MovieCollectionDetails,
    RequestCount,
    RequestCountRest,
)

urlpatterns = [
    path("register/", RegisterUser.as_view(), name="register"),
    path("login/", LoginUser.as_view(), name="login"),
    path("movies/", MovieList.as_view(), name="movies"),
    path("collection/", MovieCollection.as_view(), name="collection"),
    path(
        "collection/<str:uuid>/",
        MovieCollectionDetails.as_view(),
        name="collection-details",
    ),
    path("request-count/", RequestCount.as_view(), name="request-count"),
    path(
        "request-count/reset/", RequestCountRest.as_view(), name="request-count-reset"
    ),
]
