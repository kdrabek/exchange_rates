import pytest

from authentication.models import User


@pytest.mark.django_db
class TestUserModel(object):

    @pytest.fixture
    def test_email(self):
        return 'some@email.com'

    @pytest.fixture
    def test_password(self):
        return 'password'

    def test_creates_valid_model(self, test_email, test_password):
        user = User.objects.create_user(
            email=test_email, password=test_password)

        assert isinstance(user, User)
        assert user.email == test_email
        assert user.password is not None

    def test_user_model_representation(self, test_email, test_password):
        user = User.objects.create_user(
            email=test_email, password=test_password)

        assert str(user) == '<User email: {0}>'.format(user.email)
