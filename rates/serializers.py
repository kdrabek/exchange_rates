from rest_framework.serializers import Serializer, CharField


class CurrencySerializer(Serializer):

    code = CharField(
        required=True, allow_blank=False, trim_whitespace=True
    )
    name = CharField(
        required=True, allow_blank=False, trim_whitespace=True
    )
    table_type = CharField(
        required=True, allow_blank=False, trim_whitespace=True
    )
