from django.urls import path
from .views import RegisterView, CustomAuthToken

urlpatterns = [
    path('api/users/register/', RegisterView.as_view(), name='register'),
    path('api/users/login/', CustomAuthToken.as_view(), name='login'),
]

