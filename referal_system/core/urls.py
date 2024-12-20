from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="{Hammer Systems}",
        default_version='v1',
        description="Документация для Hammer Systems",
        contact=openapi.Contact(email="Hammer Systems"),
        license=openapi.License(name="Hammer Systems"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
    path('api/', include('api.urls')),
    path('', include('phone_numbers.urls'))
]
