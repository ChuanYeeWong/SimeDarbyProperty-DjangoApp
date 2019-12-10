from .models import Announcement
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_redis import get_redis_connection
from datetime import datetime
from notification.models import Notification
@receiver(post_save, sender=Announcement)
def create_user_profile(sender, instance, created, **kwargs):
    
    if instance.publish_datetime.date() == datetime.today().date() and instance.publish_datetime.hour == datetime.today().hour and instance.publish_datetime.minute ==  datetime.today().minute :
        #very bad :(
        re = list()
        Announcement.objects.filter(pk=instance.id).update(send_out=True)
        for b in instance.area.street_set.all():
            for c in b.lot_set.all():
                for d in c.resident_set.all():
                    if d.user.id in re:
                        pass
                    else:
                        Notification.objects.create(
                                descriptions = instance.title,
                                type = "A",
                                object_id = instance.id,
                                user_id = d.user.id,
                        )
                        re.append(d.user.id)