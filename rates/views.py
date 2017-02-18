from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rates.models import Currency, Rate
from rates.serializers import CurrencySerializer


class CurrencyView(APIView):

    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None):
        queryset = Currency.objects.all()
        queryset = self._append_query_filters(queryset, request.query_params)
        serializer = CurrencySerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def _append_query_filters(self, queryset, query_params):
        queryset = self._append_code_filter(queryset, query_params)
        return queryset

    def _append_code_filter(self, queryset, query_params):
        code = query_params.get('code')
        if code is not None:
            queryset = queryset.filter(code=code.upper())
        return queryset


class RatesView(APIView):

    def get(self, request, format=None):
        queryset = Rate.objects.all()
        serializer = CurrencySerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
