from datetime import datetime

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rates.models import Currency, Rate, Table
from rates.serializers import CurrencySerializer, RatesSerializer


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

    def get(self, request, date=None, format=None):
        table = self._get_table(date)
        queryset = Rate.objects.filter(table=table)
        serializer = RatesSerializer(queryset, many=True)

        return Response(
            {'table_date': table.date, 'rates': serializer.data},
            status=status.HTTP_200_OK,
        )

    def _get_table(self, date):
        if not date:
            return Table.objects.latest('date')
        else:
            requested_date = datetime.strptime(date, '%Y-%m-%d').date()
            return (
                Table.objects
                .filter(date__lte=requested_date)
                .order_by('-date')
                .first()
            )