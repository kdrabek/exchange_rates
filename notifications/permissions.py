from rest_framework.permissions import BasePermission

from authentication.models import User


class IsOwner(BasePermission):

    def has_permission(self, request, view):
        user_id = view.kwargs['user_id']
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return False

        return request.user == user

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
