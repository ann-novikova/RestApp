from rest_framework import permissions


class UserIsOwner(permissions.BasePermission):
    """Проверяет является ли пользователь владельцем профиля."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user
