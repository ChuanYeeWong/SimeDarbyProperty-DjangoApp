from django.db import models
from djmoney.models.fields import MoneyField
from djmoney.money import Money
from residents.models import Lot, Resident, Community, Area
from smart_selects.db_fields import ChainedForeignKey,ChainedManyToManyField
from djmoney.models.validators import MaxMoneyValidator, MinMoneyValidator
from django.core.validators import FileExtensionValidator
# Create your models here.
class BillType(models.Model):
    name = models.CharField(max_length=150)
    def __str__(self):
        return self.name
class BillSetting(models.Model):
    FREQUENT = (
        ('F', 'Every first of the month'),
        ('L', 'Every last of the month'),
        ('Q', 'Quarterly'),
        ('H', 'Half yearly'),
    )
    name = models.CharField(max_length=150)
    bill_type = models.ForeignKey(BillType,on_delete=models.CASCADE)
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency='MYR')
    specific_datetime = models.DateTimeField(null=True, blank=True, help_text="This will trigger during a specific date & time.")
    frequency = models.CharField(max_length=1, choices=FREQUENT, blank=True)
    community = models.ForeignKey(Community,on_delete=models.CASCADE)
    area = ChainedForeignKey(Area,chained_field="community",
        chained_model_field="community",
        show_all=False,
        auto_choose=False,
        sort=True)
    #lots = models.ManyToManyField(Lot, blank=True)
    lots = ChainedManyToManyField(Lot,chained_field="area",
        chained_model_field="street__area",
       )
    is_all = models.BooleanField("All Residents",default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
class Invoice(models.Model):
    STATUS = (
        ('V','Void'),
        ('P', 'Pending'),
        ('S', 'Fully Paid'),
        ('F', 'Partially Paid'),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField("Paid", default=False)
    community = models.ForeignKey(Community,on_delete=models.CASCADE)
    area = ChainedForeignKey(Area,chained_field="community",
        chained_model_field="community",
        show_all=False,
        auto_choose=False,
        sort=True)
    lot = ChainedForeignKey(Lot,chained_field="area",
        chained_model_field="street__area",
        show_all=False,
        auto_choose=False,
        sort=True)
    name = models.CharField(max_length=150)
    status = models.CharField(max_length=1, choices=STATUS, default='P')
    bill_type = models.ForeignKey(BillType,on_delete=models.CASCADE)
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency='MYR')
    bill_date = models.DateField()
    remainder = MoneyField("Outstanding Amount",max_digits=14, decimal_places=2, default_currency='MYR', default=0)
    remark = models.TextField(null=True,blank=True)
    class Meta:
        verbose_name = 'Bill'
        verbose_name_plural = 'Bill'
    def __str__(self):
        return str(self.id)
    def save(self, *args, **kwargs):
        is_create = self.pk is None
        if is_create:
            self.add_remainder(is_create,*args, **kwargs)
        super(Invoice,self).save(*args, **kwargs)
    def add_remainder(self,create,*args, **kwargs):
        self.remainder = self.amount


class Payment(models.Model):
    STATUS = (
        ('P', 'Pending'),
        ('S', 'Validated'),
        ('F', 'Invalid'),
    )
    receipt = models.ImageField("Bank Slip",upload_to='bankSlip/',validators=[FileExtensionValidator(['pdf','jpg','png'])])
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency='MYR')
    payment_date = models.DateField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True)
    status = models.CharField(max_length=1, choices=STATUS, default='P')
    updated_at = models.DateTimeField(auto_now=True,blank=True)
    invoices = models.ForeignKey(Invoice,on_delete=models.CASCADE)
    remark = models.TextField(null=True,blank=True)
    def __str__(self):
        return str(self.id)
    def save(self, *args, **kwargs):
        self.update_status(*args, **kwargs)
        super(Payment,self).save(*args, **kwargs)

    def update_status(self,*args, **kwargs):
        is_created =  self.pk is not None
        inv = self.invoices
        pay_id = None
        amt = Money(0,'MYR')
        is_pending = False
        if is_created:
            pay_id = self.pk
        for i in inv.payment_set.all():
            if(pay_id is not None and pay_id != i.pk and i.status == 'S'):
                amt += i.amount
            else:
                if(i.status =='P' and i.pk == pay_id and self.status != 'P' and is_pending == False):
                    is_pending = False
                else: 
                    if(i.status == 'P' or self.status == 'P'):
                        is_pending = True
        if(self.status == 'P'):
            is_pending = True
        if(self.status == 'S'):
            amt += self.amount
        if(amt >= inv.amount):
            inv.status = 'S'
            inv.remainder = inv.amount - amt
            inv.is_paid = True
        else:
            if (amt < inv.amount):
                inv.status = 'F'
                inv.remainder = inv.amount - amt
                inv.is_paid = True
        if is_pending:
            inv.status = 'P'
        inv.save()