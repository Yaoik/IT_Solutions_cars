from django.shortcuts import render
from rest_framework import viewsets, permissions
from .permissons import IsCarOwnerOrReadOnly, IsAuthenticatedOrReadOnly
from .serializers import CarSerializer
from .models import Car
from django.conf import settings

def main_page(request):
    """Главная страница со списком автомобилей"""
    CAR_MAX_YEAR = 2030
    CAR_MIN_YEAR = 1900
    return render(request, 'index.html', context={'CAR_MIN_YEAR':CAR_MIN_YEAR, 'CAR_MAX_YEAR':CAR_MAX_YEAR})

class CarViewSet(viewsets.ModelViewSet):
    """ViewSet для Car CRUD"""
    throttle_scope = 'car'
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsCarOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)