from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
class Notification(models.Model):
    TYPE = (
        ('A', 'Announcement'),
        ('V', 'Visitor'),
        ('B', 'Billing'),
    )
    descriptions = models.CharField(max_length=200)
    type = models.CharField(max_length=1, choices=TYPE, blank=True)
    object_id = models.IntegerField()
    is_read = models.BooleanField(default=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)