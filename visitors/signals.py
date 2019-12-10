from .models import Track_Entry
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_redis import get_redis_connection
from notification.models import Notification

@receiver(post_save, sender=Track_Entry)
def create_user_profile(sender, instance, created, **kwargs):
        if instance.entry is not None:
                if instance.entry.is_notify is not True and instance.status == "PEN" :
                        Track_Entry.objects.filter(pk=instance.id).update(status = "AIR")
                        #instance.status == "AIR"
                        #instance.save()
        if instance.lot is not None and instance.resident is not None:
                data = {"data_type":"track","track_id":instance.id, "status":instance.status,"lot":instance.lot.id,"area":instance.area.id,"resident":instance.resident.user.id}
        else:
                data = {"data_type":"track","track_id":instance.id, "status":instance.status,"lot":0,"area":instance.area.id,"resident":0}
        con = get_redis_connection("default")
        con.setex("foo",10,str(data).replace('\'','"'))
        if created:
                if instance.entry_type is not 'I' or instance.entry.is_notify is True:
                        if instance.visitor_name is None:
                                d = "A visitor has arrived"
                        else:
                                d = "Visitor "+str(instance.visitor_name)+" has arrived!"
                        Notification.objects.create(
                                descriptions = d,
                                type = "V",
                                object_id = instance.id,
                                user_id = instance.resident.user.id,
                        )
                