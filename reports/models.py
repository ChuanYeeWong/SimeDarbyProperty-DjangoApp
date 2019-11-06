from django.db import models
from billings.models import Invoice, Payment
from visitors.models import Track_Entry
# Create your models here.
class InvoiceReport(Invoice):
    class Meta:
        proxy = True
class PaymentReport(Payment):
    class Meta:
        proxy = True
class VisitReport(Track_Entry):
    class Meta:
        proxy = True