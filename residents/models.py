from django.db import models
from django.contrib.auth import get_user_model
from ordered_model.models import OrderedModel
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField
from smart_selects.db_fields import ChainedForeignKey
# Create your models here.
class Community(models.Model):
    class Meta:
        verbose_name_plural = "Communities"
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50)
    postal_code = models.IntegerField()
    city = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    description = models.TextField(null=True, blank= True)
    no_units = models.IntegerField('# of units')
    def __str__(self):
        return self.name
class Area(models.Model):
    community =  models.ForeignKey(Community,on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    thumbnail = models.ImageField(help_text="Add thumbnail.",upload_to='Area/')
    def __str__(self):
        return self.name
class Street(models.Model):
    area = models.ForeignKey(Area,on_delete=models.CASCADE)
    name = models.CharField("Street No.",max_length=150)
    def __str__(self):
        return self.name
class Lot(models.Model):
    street = models.ForeignKey(Street,on_delete=models.CASCADE,verbose_name="Street No.")
    name =  models.CharField("House No.",max_length=150)
    is_lock = models.BooleanField("Lock Property",default=False)
    class Meta:
        verbose_name = "House No."
        verbose_name_plural = 'House No.'
    def __str__(self):
        return  self.street.name +" "+self.name 
class Resident(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE,verbose_name="Resident's Name")
    lot = models.ManyToManyField(Lot,through='ResidentLotThroughModel',verbose_name="House No.")
    default_lot = models.ForeignKey(Lot,on_delete=models.CASCADE,blank=True,null=True,related_name="default_lot",verbose_name="Default House No")
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
class ResidentLotThroughModel(OrderedModel):
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE,verbose_name="House No.")
    disable_notification = models.BooleanField("Disable Notification",default=False)
    order_with_respect_to = 'lot'
    class Meta:
        ordering = ('order',)
        verbose_name = "Resident's House No"
        verbose_name_plural = "Residents's House No"
    def __str__(self):
        return self.resident.user.first_name + " " + self.resident.user.last_name

class Request(models.Model):
    STATUS = (
        ('P', 'Pending'),
        ('A', 'Approve'),
        ('R', 'Reject'),
    )
    email = models.EmailField()
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = PhoneNumberField(null=True,blank=True,)
    status = models.CharField(max_length=1, choices=STATUS, default='P')
    slip = models.ImageField("Certificate of Ownership",upload_to='images/')
    community =  models.ForeignKey(Community,on_delete=models.CASCADE)
    area = ChainedForeignKey(Area,chained_field="community",
        chained_model_field="community",
        show_all=False,
        auto_choose=False,
        sort=True)
    street =  ChainedForeignKey(Street,chained_field="area",
        chained_model_field="area",
        show_all=False,
        auto_choose=False,
        sort=True)
    lot = ChainedForeignKey(Lot,chained_field="street",
        chained_model_field="street",
        show_all=False,
        auto_choose=False,
        sort=True)
    confirm = models.BooleanField("I confirm that the information given in this form is true, complete and accurate.")
    tou = models.BooleanField("I have read and agree to the <a href='#'>Privacy Policy</a>")
    class Meta:
        verbose_name = "Resident's Request"
        verbose_name_plural = "Resident's Requests"
class RequestFamily(models.Model):
    STATUS = (
        ('P', 'Pending'),
        ('A', 'Approve'),
        ('R', 'Reject'),
    )
    email = models.EmailField()
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = PhoneNumberField(null=True,blank=True,)
    status = models.CharField(max_length=1, choices=STATUS, default='P')
    community =  models.ForeignKey(Community,on_delete=models.CASCADE)
    area = models.ForeignKey(Area,on_delete=models.CASCADE)
    street = models.ForeignKey(Street,on_delete=models.CASCADE)
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE,verbose_name="House No.")
    requestor = models.ForeignKey(Resident,on_delete=models.CASCADE)
    class Meta:
        verbose_name = "Resident's Family Request"
        verbose_name_plural = "Resident's Family Requests"

class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    phone_number = PhoneNumberField(null=True,blank=True,)
    township_community_officer_status = models.BooleanField(default=False,help_text="Designates whether the user is a township community officer.")
    community = models.ForeignKey(Community,on_delete=models.CASCADE,null=True,blank=True)
    def has_user(self):
        return self.user is not None