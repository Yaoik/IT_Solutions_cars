from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Car

class IsCarOwnerOrReadOnly(permissions.BasePermission):
    """Проверяет, является ли пользователь владельцем объекта Car."""

    def has_object_permission(self, request, view, obj:Car):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
