from .models import Announcement
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_redis import get_redis_connection

@receiver(post_save, sender=Announcement)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        data = {"id":instance.id, "status":"create","title":instance.title}
        con = get_redis_connection("default")
        con.setex("foo",10,str(data).replace('\'','"'))
    else:
        data = {"id":instance.id, "status":"update"}
        con = get_redis_connection("default")
        con.setex("foo",10,str(data).replace('\'','"'))
