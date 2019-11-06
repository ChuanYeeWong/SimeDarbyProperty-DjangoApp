from django.db import models
from residents.models import Community, Area
class Security(models.Model):
    class Meta:
        verbose_name = "Security Guard"
        verbose_name_plural = "Security Guards"
    STATUS = (
        ('A', 'Active'),
        ('I', 'Inactive'),
    )
    username = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    identity_no = models.CharField("IC/Passport No.",max_length=50,null=True,blank=True)
    password = models.CharField(max_length=255)
    salt = models.CharField(max_length=50)
    status = models.CharField(max_length=1, choices=STATUS, default='I')
    community =  models.ForeignKey(Community,on_delete=models.CASCADE)
    area = models.ForeignKey(Area,on_delete=models.CASCADE)
    

class ReasonSetting(models.Model):
    reason = models.CharField(max_length=150)
    def __str__(self):
        return self.reason
class PassNumber(models.Model):
    pass_no = models.CharField("Pass No.",max_length=150)
    community =  models.ForeignKey(Community,on_delete=models.CASCADE)
    area = models.ForeignKey(Area,on_delete=models.CASCADE)
    is_active =  models.BooleanField(default=True)
    class Meta:
        verbose_name = "Visitor Pass"
        verbose_name_plural = "Visiter Pass"
class DeviceNumber(models.Model):
    device_no = models.CharField("Device No.",max_length=150)
    community =  models.ForeignKey(Community,on_delete=models.CASCADE)
    area = models.ForeignKey(Area,on_delete=models.CASCADE)
    is_active =  models.BooleanField(default=True)
    class Meta:
        verbose_name = "Tracking Device"
        verbose_name_plural = "Tracking Devices"
class BoomgateLog(models.Model):
    security_guard = models.ForeignKey(Security,on_delete=models.CASCADE)
    STATUS = (
        ('E', 'Entry Boomgate'),
        ('X', 'Exit Boomgate'),
    )
    type = models.CharField(max_length=2, choices=STATUS, default='E')
    reason = models.ForeignKey(ReasonSetting,on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

