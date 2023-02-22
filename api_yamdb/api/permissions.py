from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOnly(BasePermission):
    """ Доступ только у пользователя с ролью admin или админа Джанго."""

    def has_permission(self, request, view):
        return request.user.is_admin or request.user.is_staff


class IsAdminOrReadOnly(BasePermission):
    """
    Доступ только у авторизованнорго пользователя
    с ролью admin или админа Джанго
    """
    message = 'Доступ только у администратора.'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.is_admin or request.user.is_staff)
        return request.method in SAFE_METHODS


class IsAuthorPermission(BasePermission):
    """ Доступ к объекту имеет автор объекта."""
    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.author == request.user)


class AdminModeratorAuthorPermission(BasePermission):
    """
    Разрешает анонимному пользователю только безопасные запросы.
    Все остальные запросы разрешаются авторизованному пользователю.
    Доступ к объекту имеют суперпользователь, админ с ролью admin
    или moderator, а также автор объекта.
    """
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
