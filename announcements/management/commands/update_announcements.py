from django.core.management.base import BaseCommand
from django.utils import timezone
from announcements.models import Announcement
from datetime import datetime
from notification.models import Notification
from django.utils import timezone
from push_notifications.models import GCMDevice
class Command(BaseCommand):
    help = 'Update Announcement'

    def handle(self, *args, **kwargs):
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