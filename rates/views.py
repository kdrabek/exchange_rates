from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status

from rates.models import Currency
from rates.serializers import CurrencySerializer


class CurrencyView(APIView):

    def get(self, request, format=None):
        queryset = Currency.objects.all()
        queryset = self._append_query_filters(queryset, request.query_params)
        json = self._prepare_json(queryset)

        return Response(json, status=status.HTTP_200_OK)

    def _prepare_json(self, queryset):
        serializer = CurrencySerializer(queryset, many=True)
        return JSONRenderer().render(serializer.data)

    def _append_query_filters(self, queryset, query_params):
        queryset = self._append_code_filter(queryset, query_params)
        return queryset

    def _append_code_filter(self, queryset, query_params):
        code = query_params.get('code')
        if code is not None:
            queryset = queryset.filter(code=code.upper())
        return queryset
