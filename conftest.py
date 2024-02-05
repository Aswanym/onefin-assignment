import pytest
from pytest_factoryboy import register
from tests.factories import UserFactory


register(UserFactory)

@pytest.fixture
def user_create(db, user_factory):
    user = user_factory.create()
    return user
