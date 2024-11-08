from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version="v1",
    ),
    public=True,
    permission_classes=(permissions.IsAdminUser,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include(("users.urls", 'users'), namespace="users")),
    path("", include(("cars.urls", 'cars'), namespace="cars")),
]

urlpatterns += [
    path("api/docs/swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("api/docs/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

