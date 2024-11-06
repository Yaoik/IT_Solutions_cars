from .views import CarViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register('', CarViewSet, basename='car')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:car_id>/comments/', include(('comments.urls', 'comments'), namespace='comments')),
]