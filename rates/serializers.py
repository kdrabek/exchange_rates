from rest_framework import serializers


class CurrencySerializer(serializers.Serializer):

    code = serializers.CharField(
        required=True, allow_blank=False, trim_whitespace=True
    )
    name = serializers.CharField(
        required=True, allow_blank=False, trim_whitespace=True
    )
    table_type = serializers.CharField(
        required=True, allow_blank=False, trim_whitespace=True
    )


class RatesSerializer(serializers.Serializer):

    currency = serializers.ReadOnlyField(source='currency.code')

    rate = serializers.DecimalField(
        required=True, decimal_places=2, max_digits=6
    )