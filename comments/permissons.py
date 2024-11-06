from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Comment

class IsCommentOwnerAndCreateOrReadOnly(permissions.BasePermission):
    """Проверяет, является ли пользователь владельцем объекта Comment."""

    def has_object_permission(self, request, view, obj:Comment):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user and request.method == 'POST'
