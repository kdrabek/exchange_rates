from rest_framework.permissions import BasePermission

from authentication.models import User


class IsOwner(BasePermission):

    def has_permission(self, request, view):
        token = view.kwargs['token']
        try:
            user = User.objects.get(auth_token__key=token)
        except User.DoesNotExist:
            return False

        return request.user == user

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
