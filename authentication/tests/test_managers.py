import pytest

from authentication.managers import UserManager
from authentication.models import User


@pytest.mark.django_db
class TestUserManager:

    @pytest.fixture
    def user_manager(self):
        manager = UserManager()
        manager.model = User
        return manager

    def test_create_user(self, user_manager):
        test_email = 'test@email.com'
        user = user_manager.create_user(test_email, 'password')

        assert user.email == test_email
        assert user.password is not None

    def test_create_user_raises_value_error_with_missing_email(
            self, user_manager):
        with pytest.raises(ValueError):
            user_manager.create_user(email=None, password='password')

    def test_create_superuser(self, user_manager):
        test_email = 'test@email.com'
        user = user_manager.create_superuser(test_email, 'password')

        assert user.email == test_email
        assert user.password is not None
        assert user.is_admin is True
