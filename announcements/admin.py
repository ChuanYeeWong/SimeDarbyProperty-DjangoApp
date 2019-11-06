from django.contrib import admin
from .models import Announcement
from jet.filters import RelatedFieldAjaxListFilter
# Register your models here.
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    search_fields = ('title', )
    list_display = ('title','community','area','publish_datetime')
    list_filter = (
        ('area', RelatedFieldAjaxListFilter),
    )