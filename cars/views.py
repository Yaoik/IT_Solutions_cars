from django.shortcuts import render
from rest_framework import viewsets, permissions
from .permissons import IsCarOwnerOrReadOnly, IsAuthenticatedOrReadOnly
from .serializers import CarSerializer
from .models import Car

def main_page(request):
    return render(request, 'index.html')

class CarViewSet(viewsets.ModelViewSet):
    """ViewSet для Car CRUD"""
    throttle_scope = 'car'
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsCarOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)