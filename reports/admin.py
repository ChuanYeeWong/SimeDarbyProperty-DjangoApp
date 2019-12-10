
from django.contrib import admin
from django.http import HttpResponse, HttpResponseForbidden
from .models import InvoiceReport,PaymentReport,VisitReport
from jet.admin import CompactInline,DefaultInline
from jet.filters import DateRangeFilter
from django.utils import timezone
import math
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
class InvoiceReportAdmin(DefaultInline):
    change_list_template = "admin/account/account_action.html"
    #list_display = ('id','lot','paid','amount')
    list_display = ('bill_no','house_no','area','amount','paid_amount','remainder','bill_type','paid','status','created_at','aging')
    list_filter = ('is_paid',('created_at', DateRangeFilter),'lot','community','area' )
    actions = ["export_as_csv"]
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def paid(self, obj):
        if(obj.is_paid):
            return "Yes"
        else:
            return "No"
    def aging(self,obj):
        now = timezone.now()
        diff= now - obj.updated_at
        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            if seconds == 1:
                return str(seconds) +  "second ago"
            else:
                return str(seconds) + " seconds ago"
        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)
            if minutes == 1:
                return str(minutes) + " minute ago"
            
            else:
                return str(minutes) + " minutes ago"
        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)
            if hours == 1:
                return str(hours) + " hour ago"
            else:
                return str(hours) + " hours ago"
        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days      
            if days == 1:
                return str(days) + " day ago"
            else:
                return str(days) + " days ago"
        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            if months == 1:
                return str(months) + " month ago"
            else:
                return str(months) + " months ago"
        if diff.days >= 365:
            years= math.floor(diff.days/365)
            if years == 1:
                return str(years) + " year ago"
            else:
                return str(years) + " years ago" 
    def paid_amount(self,obj):
        return obj.amount - obj.remainder
    def bill_no(self,obj):
        return obj.__str__()
    def house_no(self,obj):
        return obj.lot
admin.site.register(InvoiceReport,InvoiceReportAdmin)

class PaymentReportAdmin (DefaultInline):
    change_list_template = "admin/account/account_action.html"
    list_display = ('payment_no','payment_amount','bill_amount','status','payment_date','last_modified_date','last_modified')
    list_filter = ('status',('created_at', DateRangeFilter), 'invoices__area','invoices__lot','invoices__community')
    actions = ["export_as_csv"]
    def payment_no(self,obj):
        inv = InvoiceReport.objects.get(pk=obj.invoices.id)
        i = 1;
        for a in inv.payment_set.all():
            if a.id == obj.id:
                return "Inv-"+str(obj.invoices.id)+"-"+str(i)
            i = i+1
    def last_modified(self,obj):
        ct=  ContentType.objects.get(app_label='billings',model='invoice')
        a =  LogEntry.objects.filter(object_id = obj.id, content_type_id=ct.id).order_by('-action_time')
        if(a.count() > 0):
            b = get_user_model().objects.get(id = a[0].user_id)
            return b.first_name+' '+b.last_name
    def bill_amount(self,obj):
        return obj.invoices.amount
    def payment_date(self,obj):
        return obj.created_at
    def last_modified_date(self,obj):
        return obj.updated_at
    def payment_amount(self,obj):
        return obj.amount
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(PaymentReport,PaymentReportAdmin)
class VisitReportAdmin (DefaultInline):
    change_list_template = "admin/account/account_action.html"
    list_display = ('id','vehical_no','visit_address','resident','visit_time','entrytype','request_by')
    list_filter = (('created_at', DateRangeFilter),'entry_type')
    actions = ["export_as_csv"]
    def vehical_no(self,obj):
        return obj.visitor_car_plate
    def visit_address(self,obj):
        return obj.lot
    def visit_time(self,obj):
        return obj.created_at
    def entrytype(self,obj):
        if obj.entry_type == 'W':
            return 'Single Entry'
        else: 
            if obj.entry_type == 'I':
                return 'Single Entry'
        return obj.get_entry_type_display()
    def resident(self,obj):
        return obj.resident
    def request_by(self,obj):
        if obj.entry_type == 'W':
            return 'Walk In'
        else: 
            if obj.entry_type == 'I':
                return 'Impromptu'
        return 'Resident'
        
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(VisitReport,VisitReportAdmin)