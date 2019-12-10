from django.db import models
from tinymce import HTMLField
from residents.models import Area, Community
from django_redis import get_redis_connection
from smart_selects.db_fields import ChainedForeignKey
from django.core.validators import FileExtensionValidator
# Create your models here.
class Announcement(models.Model):
    title = models.CharField(max_length=150,help_text="Not more than 150 characters.")
    thumbnail = models.ImageField(upload_to='announcement/',validators=[FileExtensionValidator(['jpg','png','jpeg'])])
    body = HTMLField()
    publish_datetime = models.DateTimeField('Publish Date/Time')
    community = models.ForeignKey(Community,on_delete=models.CASCADE)
    send_out = models.BooleanField(default=False)
    area = ChainedForeignKey(Area,chained_field="community",
        chained_model_field="community",
        show_all=False,
        auto_choose=False,
        sort=True)
    def __str__(self):
        return self.title