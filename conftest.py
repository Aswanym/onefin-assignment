import pytest
from pytest_factoryboy import register
from tests.factories import UserFactory, MovieFactory, CollectionFactory


register(UserFactory)
register(MovieFactory)
register(CollectionFactory)

@pytest.fixture
def user_create(db, user_factory):
    user = user_factory.create()
    return user




