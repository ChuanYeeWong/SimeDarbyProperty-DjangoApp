from rest_framework import serializers
from announcements.models import Announcement
from datetime import datetime
class AnnouncementSerializer(serializers.ModelSerializer):
    is_new =serializers.SerializerMethodField()  
    def get_is_new(self, obj):
        res = Announcement.objects.get(pk=obj.id)
        if res.publish_datetime.date() == datetime.today().date():
            return True
        return False
    class Meta:
        model = Announcement
        fields=(
            'id',
            'title',
            'thumbnail',
            'body',
            'publish_datetime',
            'is_new',
        )
