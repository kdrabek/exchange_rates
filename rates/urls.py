from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from rates.views import CurrencyView, PingView


urlpatterns = [
    url(r'^currency', CurrencyView.as_view(), name='currency'),
    url(r'^ping', PingView.as_view(), name='ping'),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])