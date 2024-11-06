from django.shortcuts import render
from rest_framework import viewsets, permissions
from .permissons import IsCarOwnerOrReadOnly, IsAuthenticatedOrReadOnly
from .serializers import CarSerializer
from .models import Car



class CarViewSet(viewsets.ModelViewSet):
    """ViewSet для Car CRUD"""
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsCarOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)