from django.shortcuts import render
from django.core.management import execute_from_command_line
from django.http import HttpResponse
import os 
from django.utils import timezone
from datetime import datetime, timedelta
from notification.models import Notification
from django.utils import timezone
from visitors.models import Track_Entry
from django_redis import get_redis_connection
from push_notifications.models import GCMDevice
from announcements.models import Announcement

# Create your views here.
def default_view(request):
    return render(request,'users/default.html')

def auto_update_annoucement(request):
    #a = execute_from_command_line(["manage.py", "update_announcements"])
    anns = Announcement.objects.filter(publish_datetime__lte = timezone.now(),send_out = False)
    for a in anns:
        re = list()
        Announcement.objects.filter(pk=a.id).update(send_out=True)
        for b in a.area.street_set.all():
            for c in b.lot_set.all():
                for d in c.resident_set.all():
                    if d.user.id in re:
                        pass
                    else:
                        devices = GCMDevice.objects.filter(user=d.user.id)
                        devices.send_message(instance.title, extra={"type": "A","value":instance.id})
                        Notification.objects.create(
                                descriptions = a.title,
                                type = "A",
                                object_id = a.id,
                                user_id = d.user.id,
                        )
                        re.append(d.user.id)
    return HttpResponse(anns)
def auto_family(request):  
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
                con = get_redis_connection("default")
                con.setex("foo",10,str(data).replace('\'','"'))
    return HttpResponse(te)