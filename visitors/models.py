from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from residents.models import Community, Area, Resident,Lot,Street
from security_guards.models import Security,PassNumber,DeviceNumber
class Visitors(models.Model):
    name = models.CharField(max_length=150)
    car_plate = models.CharField(max_length=15)
    phone_number = PhoneNumberField()
    resident = models.ForeignKey(Resident,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
class Entry_Schedule(models.Model):
    ENTRY = (
        ('E', 'Single Entry'),
        ('M', 'Multiple Entry'),
        ('S', 'Scheduled Entry'),
    )
    lot = models.ForeignKey(Lot,on_delete = models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True,blank=True)
    is_notify = models.BooleanField(default=True)
    qr_uuid = models.CharField(max_length=150,null=True,blank=True)
    entry_type = models.CharField(max_length=1, choices=ENTRY)
    days = models.CharField(max_length=50,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    visitor_name = models.CharField(max_length=1500)
    visitor_car_plate = models.CharField(max_length=15)
    visitor_phone_number = PhoneNumberField()
    visitor = models.ForeignKey(Visitors,on_delete = models.CASCADE, null=True, blank=True)
    resident = models.ForeignKey(Resident,on_delete = models.CASCADE, null=True, blank=True )
    is_active = models.BooleanField(default=True)

class Track_Entry(models.Model):
    STATUS = (
        ('PEN','Pending entry'),
        ('AIR','Approved entry by resident'),
        ('RIR','Rejected entry by resident'),
        ('AIS','Approved entry by security guard'),
        ('RIS','Rejected entry by security guard'),
        ('PEX','Pending exit'),
        ('AOS', 'Approved exit by security guard'),
        ('ROS', 'Rejected exit by security guard'),
    )
    ENTRY = (
        ('E', 'Single Entry'),
        ('M', 'Multiple Entry'),
        ('S', 'Scheduled Entry'),
        ('W', 'Walk In'),
        ('I', 'Impromptu'),
    )
    driver_image = models.ImageField(help_text="Driver Image",upload_to='driver/')
    entry_car_plate_image = models.ImageField(help_text="Enter Carpate Image.",upload_to='entry/')
    identity_image = models.ImageField(help_text="Exit Carpate Image.",upload_to='identity/')
    exit_car_plate_image = models.ImageField(help_text="Exit Carpate Image.",upload_to='exit/',null=True,blank=True)
    status = models.CharField(max_length=3, choices=STATUS)
    entry_type = models.CharField(max_length=1, choices=ENTRY) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    visitor_name = models.CharField(max_length=150,blank=True,null=True)
    with_vehicle = models.BooleanField(default=True)
    visitor_car_plate = models.CharField(max_length=15)
    visitor_phone_number = PhoneNumberField(null=True,blank=True)
    visitor = models.ForeignKey(Visitors,on_delete = models.CASCADE, null=True, blank=True)
    entry = models.ForeignKey(Entry_Schedule,on_delete = models.CASCADE, null=True, blank=True)
    lot = models.ForeignKey(Lot,on_delete = models.CASCADE,null=True,blank=True)
    street = models.ForeignKey(Street,on_delete = models.CASCADE,null=True,blank=True)
    area = models.ForeignKey(Area,on_delete = models.CASCADE,null=True,blank=True)
    community= models.ForeignKey(Community,on_delete = models.CASCADE,null=True,blank=True)
    resident = models.ForeignKey(Resident,on_delete = models.CASCADE,null=True,blank=True)
    passNumber = models.ForeignKey(PassNumber,on_delete = models.CASCADE,null=True,blank=True)
    deviceNumber = models.ForeignKey(DeviceNumber,on_delete = models.CASCADE,null=True,blank=True)
    reason = models.CharField(max_length=150,blank=True,null=True)
    security = models.ForeignKey(Security,on_delete = models.CASCADE,null=True,blank=True)
    send_out = models.BooleanField(default=False)