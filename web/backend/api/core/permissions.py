from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff or request.method in permissions.SAFE_METHODS


class UsersMatch(permissions.BasePermission):

    def has_permission(self, request, view):
        data = request.data
        user = request.user
        return True
