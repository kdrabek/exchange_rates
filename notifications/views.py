from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import User
from rates.models import Currency
from notifications.models import Notification
from notifications.permissions import IsOwner
from notifications.serializers import NotificationSerializer


class NotificationsListView(APIView):

    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, IsOwner)

    def get(self, request, user_id, format=None):
        user = get_object_or_404(User, id=user_id)

        queryset = Notification.objects.filter(user=user)
        serializer = NotificationSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        currency = get_object_or_404(Currency, code=request.POST.get('code'))

        serializer = NotificationSerializer(data=request.POST)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save(user=user, currency=currency)
        return Response(status=status.HTTP_200_OK)


class NotificationDetailView(APIView):

    # authentication_classes = (TokenAuthentication, )
    # permission_classes = (IsAuthenticated, IsOwner)

    def get(self, request, user_id, notification_id):
        pass

    def put(self, request, user_id, notification_id):
        pass

    def delete(self, request, user_id, notification_id):
        pass
