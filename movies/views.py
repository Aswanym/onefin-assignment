from django.contrib.auth import authenticate
from django.core.cache import cache
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from decouple import config
from utility.retry_mechanism import RetryStrategy
from .serializers import (
    UserCreationSerializer,
    CollectionSerializer,
    GetCollectionSerializer,
    MovieSerializer,
)
from .models import Collection, Movies
from utility.movie_helper import TopFavouriteGenres

# Create your views here.


class LoginUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user = authenticate(
            username=request.data["username"], password=request.data["password"]
        )  # authenticate user
        if user is not None:
            token = RefreshToken.for_user(
                user
            )  # for authenticated user jwt token is created
            # refresh_token = str(token)
            access_token = str(token.access_token)
            return Response(
                {"access_token": access_token}, status=status.HTTP_201_CREATED
            )
        return Response(
            {"message": "User authentication failed"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class RegisterUser(APIView):
    """
    View for user registration.

    This view allows users to register by providing a username and password.

    Methods:
    - POST: Accepts user registration data, validates it using UserCreationSerializer,
            and creates a new user if the data is valid. After authenticate the user
            and create jwt token for that user.

    Serializer Used:
    - UserCreationSerializer: Handles the serialization and validation of user creation data.
                             Ensures secure password hashing before user creation.

    Example Usage:
    ```
    POST /register/
    {
        "username": "some_name",
        "password": "some_password"
    }
    ```

    Response (Success):
    ```
    HTTP 201 Created
    {
    "access_token": "<access_token>"
    }
    ```

    Response (Error) - invalid input:
    ```
    HTTP 400 Bad Request
    {
        "username": ["This field is required."],
        "password": ["This field is required."]
    }
    ```
    Response (Error) - authentication failed:
    ```
    HTTP 400 Bad Request
    {
        "message": "User authentication failed"
    }
    ```
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserCreationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # new user created
            user = authenticate(
                username=request.data["username"], password=request.data["password"]
            )  # authenticate user
            if user is not None:
                token = RefreshToken.for_user(
                    user
                )  # for authenticated user jwt token is created
                # refresh_token = str(token)
                access_token = str(token.access_token)
                return Response(
                    {"access_token": access_token}, status=status.HTTP_201_CREATED
                )
            return Response(
                {"message": "User authentication failed"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieList(APIView):
    """
    View for retrieving a list of movies from a third-party API.

    This view uses a RetryStrategy to handle potential issues with the third-party API.
    The API endpoint, client credentials, and retry mechanism details are obtained from
    environment variables using the python-decouple library.

    Endpoint Details:
    - URL: The URL of the third-party movie API obtained from the 'MOVIE_API_URL' environment variable.
    - Authentication: Basic auth for authentication is used. The API client credentials (username and password) obtained from the 'API_CLIENT'
      and 'API_CLIENT_SECRET' environment variables.

    Retry Mechanism:
    - The RetryStrategy.retry_mechanism method is called to make the API request with built-in retry logic.
      This helps handle potential flakiness or timeouts of the third-party API.

    Example Usage:
    ```
    GET /movies/
    ```

    Response (Success):
    ```
    HTTP 200 OK
    {
         "count": <total number of movies>,
         "next": <link for next page, if present>,
         "previous": <link for previous page>,
         "data": [
             {
                 "title": <title of the movie>,
                 "description": <a description of the movie>,
                 "genres": <a comma separated list of genres, if present>,
                 "uuid": <a unique uuid for the movie>
             },
             ...
         ]
     }

    ```
    Response (Error):
    ```
    HTTP 200 OK
    {
         "message": "Failed to load movies, please try again.",
         "status_code": 500
     }
    ```

    Environment Variables:
    - MOVIE_API_URL: The URL of the third-party movie API.
    - API_CLIENT: API client username.
    - API_CLIENT_SECRET: API client password.

    Dependencies:
    - RetryStrategy: A custom class or module providing retry mechanisms for API requests.

    """

    def get(self, request):
        url = config("MOVIE_API_URL")
        username = config("API_CLIENT")
        password = config("API_CLIENT_SECRET")

        api_res = RetryStrategy.retry_mechanism(
            url, username=username, password=password, verify=False
        )
        return Response(api_res)


class MovieCollection(generics.ListCreateAPIView):
    """
    A view for handling the retrieval and creation of movie collections.

    - GET: Retrieve a user's movie collections along with their top 3 favorite genres.
      Response includes serialized collection data and favorite genres.

    - POST: Create a new movie collection for the authenticated user.
      Request data should include title, description, and a list of movies
      with UUID, title, description, and genres.

    Parameters:
    - `request`: The HTTP request object.
    - `*args`: Additional positional arguments.
    - `**kwargs`: Additional keyword arguments.

    Returns:
    - For GET: Serialized data of user's collections and top 3 favorite genres.
    - For POST: A response containing the UUID of the newly created collection.

    Example GET Response:
    ```
    {
        "is_success": True,
        "data": {"collection": [...serialized collection data...]},
        "favourite_genres": ["Horror", "Action", "Comedy"]
    }
    ```

    Example POST Response:
    ```
    {
        "collection_uuid": "ae5ef1d4-5d02-4f11-8d61-8d3b5dfc4b8b"
    }
    ```

    Raises:
    - HTTP 200 OK for successful GET requests.
    - HTTP 201 Created for successful POST requests.
    """

    def get(self, request, *args, **kwargs):
        collections = Collection.objects.filter(user=request.user)
        serializer = GetCollectionSerializer(collections, many=True)

        collection_list = {"collection": serializer.data}
        favourite_genres = (
            TopFavouriteGenres().top_favourite_genres_from_user_movie_collection(
                collections, n=3
            )
        )

        context = {
            "is_success": True,
            "data": collection_list,
            "favourite_genres": favourite_genres,
        }
        return Response(context, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data
        new_collection = Collection.objects.create(
            title=data["title"], description=data["description"], user=request.user
        )  # create a collection
        new_collection.save()

        # iterate through list of movies, if movies not in db create, else get that movie obj and add it to the
        # above created collection.
        for movie in data["movies"]:
            if Movies.objects.filter(uuid=movie["uuid"]).exists():
                movie_obj = Movies.objects.get(uuid=movie["uuid"])
            else:
                movie_obj = Movies.objects.create(
                    uuid=movie["uuid"],
                    title=movie["title"],
                    description=movie["description"],
                    genres=movie["genres"],
                )

            new_collection.movies.add(movie_obj)

        serializer = CollectionSerializer(new_collection)
        context = {"collection_uuid": serializer.data["uuid"]}
        return Response(context, status=status.HTTP_201_CREATED)


class MovieCollectionDetails(generics.RetrieveUpdateDestroyAPIView):
    """
    A view for retrieving, updating, and deleting a movie collection.

    - GET: Retrieve details of a movie collection, including title, description, and associated movies.

    - PUT/PATCH: Update a movie collection's details and associated movies. The request should include
      optional fields such as 'title', 'description', and 'movies' (a list of movies with UUID, title,
      description, and other details).

    - DELETE: Delete a movie collection.

    Parameters:
    - `request`: The HTTP request object.
    - `*args`: Additional positional arguments.
    - `**kwargs`: Additional keyword arguments.

    Returns:
    - For GET: Serialized data of the movie collection and associated movies.
    - For PUT/PATCH: A response indicating that the movie collection was updated.
    - For DELETE: A response indicating that the movie collection was successfully deleted.

    Example GET Response:
    ```
    {
        "title": "Collection title",
        "description": "Collection description",
        "movies": [
            {"uuid": "movie_uuid_1", "title": "Movie 1", "description": "description 1", "genre":genre1},
            {"uuid": "movie_uuid_2", "title": "Movie 2", "description": "description 2", "genre":genre2},
            ...
        ]
    }
    ```

    Example PUT/PATCH Request:
    ```
    {
        "title": "Updated Collection",
        "description": "Updated description",
        "movies": [
            {"uuid": "movie_uuid_1", "title": "Updated Movie 1", "description": "Updated description 1", ...},
            {"uuid": "movie_uuid_2", "title": "Updated Movie 2", "description": "Updated description 2", ...},
            ...
        ]
    }
    ```

    Example PUT/PATCH Response:
    ```
    {"details": "updated"}
    ```

    Example DELETE Response:
    ```
    {"detail": "Successfully deleted."}
    ```
    """

    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    lookup_field = "uuid"

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # include needed data in the context
        movies_data = MovieSerializer(instance.movies.all(), many=True).data
        context = {
            "title": serializer.data["title"],
            "description": serializer.data["description"],
            "movies": movies_data,
        }
        return Response(context, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        if "movies" in request.data:
            movies = request.data.pop("movies")
            for movie in movies:
                movie_instance = Movies.objects.get(uuid=movie["uuid"])
                movie_serializer = MovieSerializer(
                    movie_instance, data=movie, partial=True
                )
                movie_serializer.is_valid(raise_exception=True)
                self.perform_update(movie_serializer)

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"details": "updated"})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Successfully deleted."}, status=status.HTTP_204_NO_CONTENT
        )


class RequestCount(APIView):
    def get(self, request, *args, **kwargs):
        request_count = cache.get("request_count")
        context = {"requests": request_count}
        return Response(context, status=status.HTTP_200_OK)


class RequestCountRest(APIView):
    def post(self, request, *args, **kwargs):
        cache.set("request_count", 0)
        context = {"message": "request count reset successfully"}
        return Response(context, status=status.HTTP_200_OK)
