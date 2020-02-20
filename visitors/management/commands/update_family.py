from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from notification.models import Notification
from django.utils import timezone
from visitors.models import Track_Entry
from django_redis import get_redis_connection
from push_notifications.models import GCMDevice
class Command(BaseCommand):
    help = 'Send to Family Member'

    def handle(self, *args, **kwargs):
        te = Track_Entry.objects.filter(created_at__gte = (timezone.now()- timedelta(seconds=60)),status="PEN",send_out=False) 
        #te = Track_Entry.objects.filter(pk=138)
        for t in te.all():
            Track_Entry.objects.filter(pk=t.id).update(send_out=True)
            for rlt in t.lot.residentlotthroughmodel_set.all():        
                if t.entry_type is not 'I' and rlt.disable_notification is False and rlt.resident.id != t.resident.id :
                    print(rlt.resident.user.id)
                    if t.visitor_name is None:
                        d = "A visitor has arrived"
                    else:
                        d = "Visitor "+str(t.visitor_name)+" has arrived!"
                    devices = GCMDevice.objects.filter(user=instance.resident.user.id)
                    devices.send_message(d,extra={"type": "V","value":instance.id})
                    Notification.objects.create(
                            descriptions = d,
                            type = "V",
                            object_id = t.id,
                            user_id = rlt.resident.user.id,
                    )
                    
                    data = {"data_type":"update","track_id":t.id, "status":t.status,"lot":0,"area":t.area.id,"resident":rlt.resident.user.id}
                    #con = get_redis_connection("default")
                    con = redis.StrictRedis(host='vmswebcache.redis.cache.windows.net',
        port=6380, db=0, password='IsF++8DTZ01nNN3Ec5b5FS9xxoZYRD4Qs+UvG6FB5ew=', ssl=True)
                    con.setex("foo",10,str(data).replace('\'','"'))

