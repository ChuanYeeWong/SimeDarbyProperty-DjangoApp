from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from notification.models import Notification
from django.utils import timezone
from visitors.models import Track_Entry
from django_redis import get_redis_connection
class Command(BaseCommand):
    help = 'Send to Family Member'

    def handle(self, *args, **kwargs):
       # te = Track_Entry.objects.filter(created_at__gte = (datetime.now()- timedelta(seconds=60)),created_at__lte = (datetime.now() -  timedelta(seconds=120)),status="PEN") 
        te = Track_Entry.objects.filter(created_at__gte = (timezone.now()- timedelta(seconds=60)),status="PEN")
        for t in te.all():
            for rlt in t.lot.residentlotthroughmodel_set.all():
                 if t.entry_type is not 'I' and rlt.disable_notification is False and rlt.resident.id != t.resident.id :
                     print(rlt.resident.user)