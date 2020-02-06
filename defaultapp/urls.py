from django.conf.urls import url
from . import views
from django.urls import path,include
from . import views
urlpatterns = [
    url('aua/',views.auto_update_annoucement),
    url('af/',views.auto_family),
    url('',views.default_view),
    
]