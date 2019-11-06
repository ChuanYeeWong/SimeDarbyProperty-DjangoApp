from django.conf.urls import url
from . import views
from django.urls import path,include
urlpatterns = [
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='user-activate'), 
    url(r'^terms/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.confirm_terms, name='user-terms'),
    path('register/', views.request_resident, name='register'),
    path('register-complete/', views.request_complete, name='register_complete'),
]