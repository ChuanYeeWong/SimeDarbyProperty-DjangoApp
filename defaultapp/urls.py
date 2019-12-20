from django.conf.urls import url
from . import views
from django.urls import path,include
from . import views
urlpatterns = [
    url('',views.default_view)
]