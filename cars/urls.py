from .views import CarViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import main_page

router = DefaultRouter()
router.register('', CarViewSet, basename='car')

urlpatterns = [
    path('api/cars/', include(router.urls)),
    path('api/cars/<int:car_id>/comments/', include(('comments.urls', 'comments'), namespace='comments')),
]

urlpatterns += [
    path('', main_page, name='index')
]