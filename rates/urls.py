from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from rates.views import CurrencyView, RatesView, RateDetailsView


urlpatterns = [
    url(r'^currency', CurrencyView.as_view(), name='currency'),
    url(r'^rates/(?P<date>[0-9-]+)', RatesView.as_view(),
        name='rates_for_date'),
    url(r'rates/(?P<currency_code>[A-Z]+)/limit/(?P<limit>[0-9]+)',
        RateDetailsView.as_view(), name='rate_detail_view'),
    url(r'^rates', RatesView.as_view(), name='rates_latest'),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])