import pytest
import mock

from authentication.models import User
from notifications.models import Notification
from notifications.permissions import IsOwner
from rates.models import Currency


@pytest.mark.django_db
class TestIsOwnerPermission:

    @pytest.fixture
    def mock_request(self, user):
        return mock.MagicMock(user=user)

    @pytest.fixture
    def mock_view(self, user):
        return mock.MagicMock(kwargs={'user_id': user.id})

    def test_has_object_permission_when_owner(
            self, mock_request, notification):
        has_permission = IsOwner().has_object_permission(
            mock_request, view=None, obj=notification)

        assert has_permission is True

    def test_has_object_permission_when_not_owner(
            self, mock_request, another_user, notification):
        mock_request.user = another_user
        has_permission = IsOwner().has_object_permission(
            mock_request, view=None, obj=notification)
        assert has_permission is False

    def test_has_permission_when_accessing_self_view(
            self, mock_request, mock_view):
        has_permission = IsOwner().has_permission(mock_request, view=mock_view)
        assert has_permission is True

    def test_has_permission_when_accessing_other_user_view(
            self, mock_request, mock_view, another_user):
        mock_view.kwargs = {'user_id': another_user.id}
        has_permission = IsOwner().has_permission(mock_request, view=mock_view)
        assert has_permission is False

    def test_has_permission_when_user_does_not_exist(
            self, mock_request, mock_view, user):
        mock_view.kwargs = {'user_id': user.id + 1}
        has_permission = IsOwner().has_permission(mock_request, view=mock_view)
        assert has_permission is False
