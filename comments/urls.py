from rest_framework.routers import DefaultRouter
from .views import CommentViewSet
from django.urls import path, include

router = DefaultRouter()
router.register('', CommentViewSet, basename='comment')

app_name = 'comments'

urlpatterns = router.urls