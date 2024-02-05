import pytest
from django.contrib.auth.models import User

@pytest.mark.customers
class TestUserRegistration(object):

    @pytest.mark.tcid29
    @pytest.mark.django_db
    def test_user_registration_success(self, user):

        # check user generated
        assert user is not None, "User not created successfully"

        # Check if the access_token is generated
        assert user.access_token, "Access token not generated"

