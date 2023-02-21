from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_admin or request.user.is_staff)


class IsAdminOrReadOnly(BasePermission):
    message = 'Доступ только у администратора.'

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return (request.user.is_admin or request.user.is_staff)


class IsAuthorPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.author == request.user)


class AdminModeratorAuthorPermission(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )
