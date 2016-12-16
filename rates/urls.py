from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from rates.views import CurrencyView


urlpatterns = [
    url(r'^currency', CurrencyView.as_view(), name='currency'),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])