from django.urls import path
from .views import RegisterView, CustomAuthToken, register_form

urlpatterns = [
    path('api/users/register/', RegisterView.as_view(), name='register'),
    path('api/users/login/', CustomAuthToken.as_view(), name='login'),
]

urlpatterns += [
    path('register/', register_form, name='register_form')
]
