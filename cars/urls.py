from django.contrib import admin
from django.urls import path
from .views import CarViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', CarViewSet, basename='car')

urlpatterns = router.urls