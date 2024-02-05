import pytest
from ..factories import UserFactory, CollectionFactory, MovieFactory

# this test is not completed
class TestGetCollection(object):
    @pytest.mark.tcid31
    @pytest.mark.django_db
    def test_get_collection_api(self):
        # Create a user instance
        user_instance = UserFactory()

        # Create a collection instance associated with the user
        collection_instance = CollectionFactory(user=user_instance)

        assert True