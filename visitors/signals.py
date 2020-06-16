from .models import Track_Entry
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_redis import get_redis_connection
from notification.models import Notification
from push_notifications.models import GCMDevice
import redis
@receiver(post_save, sender=Track_Entry)
def create_user_profile(sender, instance, created, **kwargs):
        notify = False
        id = -1
        if instance.entry is not None:
                notify = instance.entry.is_notify
                if instance.entry.is_notify is not True and instance.status == "PEN" :
                        Track_Entry.objects.filter(pk=instance.id).update(status = "AIR")
                        #instance.status == "AIR"
                        #instance.save()
        if created:
                if instance.entry_type is not 'I' or notify:
                        if instance.visitor_name is None:
                                d = "A visitor has arrived"
                        else:
                                d = "Visitor "+str(instance.visitor_name)+" has arrived!"
                        devices = GCMDevice.objects.filter(user=instance.resident.user.id)
                        devices.send_message(d,extra={"type": "V","value":instance.id})
                        n = Notification.objects.create(
                                descriptions = d,
                                type = "V",
                                object_id = instance.id,
                                user_id = instance.resident.user.id,
                        )
                        id = n.pk
        if instance.lot is not None and instance.resident is not None:
                data = {"data_type":"track","track_id":instance.id, "status":instance.status,"lot":instance.lot.id,"area":instance.area.id,"resident":instance.resident.user.id , 'noti_id':id}
        else:
                data = {"data_type":"track","track_id":instance.id, "status":instance.status,"lot":0,"area":instance.area.id,"resident":0, 'noti_id':id}
        con = redis.StrictRedis(host='vmswebcache.redis.cache.windows.net',
        port=6380, db=0, password='IsF++8DTZ01nNN3Ec5b5FS9xxoZYRD4Qs+UvG6FB5ew=', ssl=True)
        #con = get_redis_connection("default")
        con.setex("foo",10,str(data).replace('\'','"'))
        
        
# def create_user_profile(sender, instance, created, **kwargs):
#         notify = False
#         if instance.entry is not None:
#                 notify = instance.entry.is_notify
#                 if instance.entry.is_notify is not True and instance.status == "PEN" :
#                         Track_Entry.objects.filter(pk=instance.id).update(status = "AIR")
#                         #instance.status == "AIR"
#                         #instance.save()
#         if instance.lot is not None and instance.resident is not None:
#                 data = {"data_type":"track","track_id":instance.id, "status":instance.status,"lot":instance.lot.id,"area":instance.area.id,"resident":instance.resident.user.id}
#         else:
#                 data = {"data_type":"track","track_id":instance.id, "status":instance.status,"lot":0,"area":instance.area.id,"resident":0}
#         con = redis.StrictRedis(host='vmswebcache.redis.cache.windows.net',
#         port=6380, db=0, password='IsF++8DTZ01nNN3Ec5b5FS9xxoZYRD4Qs+UvG6FB5ew=', ssl=True)
#         #con = get_redis_connection("default")
#         con.setex("foo",10,str(data).replace('\'','"'))
#         if created:
#                 if instance.entry_type is not 'I' or notify:
#                         if instance.visitor_name is None:
#                                 d = "A visitor has arrived"
#                         else:
#                                 d = "Visitor "+str(instance.visitor_name)+" has arrived!"
#                         devices = GCMDevice.objects.filter(user=instance.resident.user.id)
#                         devices.send_message(d,extra={"type": "V","value":instance.id})
#                         Notification.objects.create(
#                                 descriptions = d,
#                                 type = "V",
#                                 object_id = instance.id,
#                                 user_id = instance.resident.user.id,
#                         )
                
