from rest_framework import serializers

from notifications.models import Notification


class NotificationSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    token = serializers.ReadOnlyField(source='user.auth_token.key')
    currency = serializers.ReadOnlyField(source='currency.code')
    rate = serializers.DecimalField(
        required=True, decimal_places=2, max_digits=6)
    threshold = serializers.CharField(required=True, trim_whitespace=True)
    is_active = serializers.BooleanField()


    def create(self, validated_data):
        return Notification.objects.create(**validated_data, last_sent=None)

    def update(self, instance, validated_data):
        instance.rate = validated_data.get('rate', instance.rate)
        instance.threshold = validated_data.get('threshold', instance.threshold)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance