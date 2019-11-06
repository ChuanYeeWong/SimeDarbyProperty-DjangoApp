from django.contrib.auth import get_user_model
from rest_framework import serializers
from notification.models import Notification
#user module serializer
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            'id',
            'descriptions',
            'type',
            'object_id',
            'user',
            'is_read',
            'created_at',
        )
