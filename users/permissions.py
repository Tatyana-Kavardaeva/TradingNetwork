from rest_framework import permissions


class IsActive(permissions.BasePermission):
    """ Проверяет статус активности пользователя 'is_active'. """

    def has_permission(self, request, view):
        return request.user.is_active

    def has_object_permission(self, request, view, obj):
        return request.user.is_active
