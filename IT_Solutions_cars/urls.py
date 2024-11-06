from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/users/", include(("users.urls", 'users'), namespace="users")),
    path("api/cars/", include(("cars.urls", 'cars'), namespace="cars")),
]
