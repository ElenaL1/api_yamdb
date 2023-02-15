from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    message = 'Доступ только у администратора.'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if self.user.is_staff:
            return True
