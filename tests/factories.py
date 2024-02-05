import factory
import uuid
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from movies.models import Collection, Movies

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    password = factory.Faker('password')

    @classmethod
    def create(cls, **kwargs):
        user = super().create(**kwargs)
        # Generate JWT token for the user
        refresh_token = RefreshToken.for_user (user)
        user.access_token = str(refresh_token.access_token)
        return user


class MovieFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Movies

    # Define movie fields with either static or dynamic data

    uuid = uuid.uuid4()  # You can set a specific UUID or use the default one
    title = factory.Faker('sentence')
    description = factory.Faker('text')
    genres = factory.Faker('word')


class CollectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Collection

    # Define collection fields with either static or dynamic data
    uuid = uuid.uuid4()
    title = factory.Faker ('sentence')
    description = factory.Faker ('text')
    user = factory.SubFactory(UserFactory)
    movies = factory.SubFactory(MovieFactory)

