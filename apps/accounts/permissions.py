from rest_framework import permissions


class IsMerchant(permissions.BasePermission):
    message = "You are not allowed to perform this action"

    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated and request.user.is_merchant
        )
