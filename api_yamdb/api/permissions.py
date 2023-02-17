from rest_framework.permissions import BasePermission, SAFE_METHODS


class AdminOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff


class IsAdminOrReadOnly(BasePermission):
    message = 'Доступ только у администратора.'

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff


class IsAuthorPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.author == request.user)
