from django.db.models.signals import post_save
from django.dispatch import receiver
from django_redis import get_redis_connection
from datetime import datetime
from .models import RequestFamily
from notification.models import Notification
from push_notifications.models import GCMDevice
@receiver(post_save, sender=RequestFamily)
def create_user_profile(sender, instance, created, **kwargs):
    if instance.status != 'P':
        if instance.status == 'A':
            a = "approved"
        else:
            a = "rejected"
        devices = GCMDevice.objects.filter(user=instance.requestor.user.id)
        devices.send_message("Your request for "+instance.first_name+" "+instance.last_name+" has been "+a)
        Notification.objects.create(
                descriptions = "Your request for "+instance.first_name+" "+instance.last_name+" has been "+a,
                type = "F",
                object_id = instance.id,
                user_id = instance.requestor.user.id,
        )