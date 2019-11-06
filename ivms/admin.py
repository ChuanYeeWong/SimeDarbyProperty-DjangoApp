from django.contrib import admin
from .models import IPCamera,Boomgate
# Register your models here.

@admin.register(IPCamera)
class IPCameraAdmin(admin.ModelAdmin):
    search_fields = ('url', )
    list_display = ('url','type','community','area')

@admin.register(Boomgate)
class BoomgateAdmin(admin.ModelAdmin):
    search_fields = ('url', )
    list_display = ('url','type','community','area')