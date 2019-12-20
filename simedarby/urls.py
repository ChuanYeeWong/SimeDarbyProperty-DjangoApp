"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls import url
admin.site.site_header = 'Sime Darby'
admin.site.site_title = 'Sime Darby'
admin.site.site_url = ''
schema_view = get_schema_view(
    openapi.Info(
        title="IVMS API",
        default_version='v1',
        description="",
        terms_of_service="",
        contact=openapi.Contact(email="support@lcpbuildsofttechnology.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticated,),
)
urlpatterns = [
    path('admin/', admin.site.urls,name="admin"),
    path('jet/',include('jet.urls','jet')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('user/',include('users.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('v1/',include('api.urls')),
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('chaining/', include('smart_selects.urls')),
    path('',include('defaultapp.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
