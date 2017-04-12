from rest_framework import serializers


class CurrencySerializer(serializers.Serializer):

    code = serializers.CharField(
        required=True, allow_blank=False, trim_whitespace=True)
    name = serializers.CharField(
        required=True, allow_blank=False, trim_whitespace=True)
    country = serializers.ReadOnlyField()
    table_type = serializers.CharField(
        required=True, allow_blank=False, trim_whitespace=True)


class RatesSerializer(serializers.Serializer):

    currency = serializers.ReadOnlyField(source='currency.code')
    country = serializers.ReadOnlyField(source='currency.country')
    name = serializers.ReadOnlyField(source='currency.name')
    rate = serializers.DecimalField(
        required=True, decimal_places=4, max_digits=6)


class RateDetailsSerializer(RatesSerializer):

    date = serializers.ReadOnlyField(source='table.date')
    relative_change = serializers.DecimalField(
        required=True, decimal_places=4, max_digits=6)
