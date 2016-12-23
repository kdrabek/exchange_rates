from django.shortcuts import get_object_or_404
from django.utils.six import BytesIO

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import User
from rates.models import Currency
from notifications.models import Notification
from notifications.permissions import IsOwner
from notifications.serializers import NotificationSerializer


def get_json(request):
    stream = BytesIO(request.body)
    return JSONParser().parse(stream)


class NotificationsListView(APIView):

    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, IsOwner)

    def get(self, request, user_id, format=None):
        user = get_object_or_404(User, id=user_id)

        queryset = Notification.objects.filter(user=user)
        serializer = NotificationSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, user_id):
        data = get_json(request)
        user = get_object_or_404(User, id=user_id)
        currency = get_object_or_404(Currency, code=data.get('code'))

        serializer = NotificationSerializer(data=data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save(user=user, currency=currency)
        return Response(status=status.HTTP_200_OK)


class NotificationDetailView(APIView):

    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, IsOwner)

    def get(self, request, user_id, notification_id):
        user = get_object_or_404(User, id=user_id)
        notification = get_object_or_404(Notification, id=notification_id)
        serializer = NotificationSerializer(notification)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, user_id, notification_id):
        user = get_object_or_404(User, id=user_id)
        notification = get_object_or_404(Notification, id=notification_id)
        data = get_json(request)
        serializer = NotificationSerializer(notification, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id, notification_id):
        user = get_object_or_404(User, id=user_id)
        notification = get_object_or_404(Notification, id=notification_id)
        notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
