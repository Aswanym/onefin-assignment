from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserCreationSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

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
    def post(self, request):
        serializer = UserCreationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # new user created
            user = authenticate(username=request.data['username'], password=request.data['password'])  # authenticate user
            if user is not None:
                token = RefreshToken.for_user(user)  # for authenticated user jwt token is created
                # refresh_token = str(token)
                access_token = str(token.access_token)
                return Response({"access_token": access_token}, status=status.HTTP_201_CREATED)
            return Response({"message": "User authentication failed"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


