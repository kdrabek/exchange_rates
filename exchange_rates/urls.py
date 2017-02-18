from django.conf.urls import url, include

urlpatterns = [
    url(
        r'^auth/',
        include('authentication.urls', namespace='auth')
    ),
    url(
        r'^rates/',
        include('rates.urls', namespace='rates')
    ),
    url(
        r'^notifications/',
        include('notifications.urls', namespace='notifications')
    ),
]
