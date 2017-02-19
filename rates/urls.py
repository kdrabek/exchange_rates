from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from rates.views import CurrencyView, RatesView


urlpatterns = [
    url(r'^currency', CurrencyView.as_view(), name='currency'),
    url(r'^rates/(?P<date>[0-9-]+)', RatesView.as_view(),
        name='rates_for_date'),
    url(r'^rates', RatesView.as_view(), name='rates_latest'),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])