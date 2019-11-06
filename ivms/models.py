from django.db import models
from residents.models import Community, Area
from smart_selects.db_fields import ChainedForeignKey
class IPCamera(models.Model):
    class Meta:
        verbose_name_plural = "IP Camera Settings"
    STATUS = (
        ('EF', 'Entry Front Camera'),
        ('EB', 'Entry Back Camera'),
        ('IC', 'IC Camera'),
        ('XF', 'Exit Front Camera'),
        ('XB', 'Exit Back Camera'),
        ('FC', 'Face Camera')
    )
    url = models.CharField(max_length=255)
    type = models.CharField(max_length=2, choices=STATUS, default='EF')
    community =  models.ForeignKey(Community,on_delete=models.CASCADE)
    area = ChainedForeignKey(Area,chained_field="community",
        chained_model_field="community",
        show_all=False,
        auto_choose=False,
        sort=True)

class Boomgate(models.Model):
    class Meta:
        verbose_name_plural = "Boomgate Settings"
    STATUS = (
        ('E', 'Entry Boomgate'),
        ('X', 'Exit Boomgate'),
    )
    url = models.CharField(max_length=255)
    type = models.CharField(max_length=2, choices=STATUS, default='E')
    community =  models.ForeignKey(Community,on_delete=models.CASCADE)
    area = ChainedForeignKey(Area,chained_field="community",
        chained_model_field="community",
        show_all=False,
        auto_choose=False,
        sort=True)