from rest_framework.permissions import BasePermission

from App.models import AXFUser


class UserLoginPermission(BasePermission):

    def has_permission(self, request, view):

        if type(view).__name__ == "AXFUserAPIView" and request.method == "POST":
            return True

        return isinstance(request.user, AXFUser)

    def has_object_permission(self, request, view, obj):
        return True
