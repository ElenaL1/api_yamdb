from rest_framework.permissions import BasePermission
from rest_framework import permissions


class IsAdminOrReadOnly(BasePermission):
    message = 'Доступ только у администратора.'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff


class IsAuthorPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)
