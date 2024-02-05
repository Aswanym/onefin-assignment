import factory
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

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




