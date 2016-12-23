from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from notifications.views import NotificationsListView, NotificationDetailView


urlpatterns = [
    url(r'(?P<user_id>[0-9]+)/(?P<notification_id>[0-9]+)$',
        NotificationDetailView.as_view(), name='detail'),
    url(r'(?P<user_id>[0-9]+)$', NotificationsListView.as_view(), name='list'),

]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])