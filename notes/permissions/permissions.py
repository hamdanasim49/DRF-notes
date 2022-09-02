from rest_framework import permissions


class UserPermission(permissions.BasePermission):
    edit_methods = ("POST", "PUT", "PATCH")

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return False
        else:
            return True
