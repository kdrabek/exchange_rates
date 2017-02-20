import pytest

from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.renderers import JSONRenderer


from notifications.models import Notification


@pytest.mark.django_db
class TestNotificationsListView(object):

    @pytest.fixture
    def post_data(self):
        return {
            'code': 'AUD',
            'rate': '23.45',
            'threshold': 'ABOVE',
            'is_active': True
        }

    def assert_response(self, response, expected_len, expected_keys):
        data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(data, list)
        assert len(data) == expected_len

        if expected_len > 0:
            assert isinstance(data[0], dict)
            assert sorted(expected_keys) == sorted(data[0].keys())

    def test_unauthenticated_user_is_unauthorized(self, client, user):
        response = client.get(
            reverse('notifications:list', kwargs={'user_id': user.id})
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authenticated_user_cannot_access_another_users_resource(
            self, client, user, token):
        response = client.get(
            reverse('notifications:list', kwargs={'user_id': user.id + 1}),
            HTTP_AUTHORIZATION='Token {0}'.format(token)
        )

        assert  response.status_code == status.HTTP_403_FORBIDDEN

    def test_authenticated_user_can_get_notification_list(
            self, client, user, token, notification):
        response = client.get(
            reverse('notifications:list', kwargs={'user_id': user.id}),
            HTTP_AUTHORIZATION='Token {0}'.format(token)
        )

        self.assert_response(
            response, expected_len=1,
            expected_keys=[
                'id', 'currency', 'rate', 'threshold', 'user', 'is_active'
            ]
        )

    def test_authenticated_user_can_create_new_notification(
            self, client, user, token, currency, post_data):
        response = client.post(
            reverse('notifications:list', kwargs={'user_id': user.id}),
            JSONRenderer().render(post_data),
            content_type="application/json",
            HTTP_AUTHORIZATION='Token {0}'.format(token)
        )

        assert response.status_code == status.HTTP_200_OK
        assert Notification.objects.filter(user=user).count() == 1

    def test_404_raised_when_invalid_currency(
            self, client, user, token, currency, post_data):
        post_data['code'] = 'XXX'
        response = client.post(
            reverse('notifications:list', kwargs={'user_id': user.id}),
            JSONRenderer().render(post_data),
            content_type="application/json",
            HTTP_AUTHORIZATION='Token {0}'.format(token)
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert Notification.objects.filter(user=user).count() == 0

    def test_bad_request_raised_when_invalid_post_data(
            self, client, user, token, currency, post_data):
        post_data['rate'] = '1.23456'  # to many decimal places
        response = client.post(
            reverse('notifications:list', kwargs={'user_id': user.id}),
            JSONRenderer().render(post_data),
            content_type="application/json",
            HTTP_AUTHORIZATION='Token {0}'.format(token)
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert Notification.objects.filter(user=user).count() == 0


@pytest.mark.django_db
class TestNotificationsDetailView(object):

    @pytest.fixture
    def put_data(self):
        return {
            'code': 'AUD',
            'rate': '23.45',
            'threshold': 'BELOW',
            'is_active': False
        }

    def test_get_unauthenticated_user(self, client, user, token):
        response = client.get(
            reverse(
                'notifications:detail',
                kwargs={'user_id': user.id, 'notification_id': 1}
            )
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_single_notification(self, client, user, token, notification):
        response = client.get(
            reverse(
                'notifications:detail',
                kwargs={'user_id': user.id, 'notification_id': notification.id}
            ),
            HTTP_AUTHORIZATION='Token {0}'.format(token)
        )

        data = response.json()
        expected_keys = [
            'id', 'currency', 'rate', 'threshold', 'user', 'is_active'
        ]

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(data, dict)
        assert sorted(expected_keys) == sorted(data.keys())

    def test_put_single_notification(
            self, client, user, token, notification, put_data):
        response = client.put(
            reverse(
                'notifications:detail',
                kwargs={'user_id': user.id, 'notification_id': notification.id}
            ),
            JSONRenderer().render(put_data),
            content_type="application/json",
            HTTP_AUTHORIZATION='Token {0}'.format(token)
        )
        updated_notification = Notification.objects.get(id=notification.id)

        assert response.status_code == status.HTTP_200_OK
        assert str(notification.rate) == '12.34'
        assert notification.threshold == 'ABOVE'
        assert str(updated_notification.rate) == put_data['rate']
        assert updated_notification.threshold == put_data['threshold']
        assert updated_notification.is_active is put_data['is_active']

    def test_delete_single_notification(
            self, client, user, token, notification):
        response = client.delete(
            reverse(
                'notifications:detail',
                kwargs={'user_id': user.id, 'notification_id': notification.id}
            ),
            HTTP_AUTHORIZATION='Token {0}'.format(token)
        )
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        with pytest.raises(Notification.DoesNotExist):
            Notification.objects.get(id=notification.id)
