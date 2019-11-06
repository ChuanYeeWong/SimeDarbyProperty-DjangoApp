
from django.contrib import admin
from django.http import HttpResponse, HttpResponseForbidden
from .models import InvoiceReport,PaymentReport,VisitReport
from jet.admin import CompactInline,DefaultInline
from jet.filters import DateRangeFilter


class InvoiceReportAdmin(DefaultInline):
    change_list_template = "admin/account/account_action.html"
    list_display = ('id','lot','paid','amount')
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
admin.site.register(InvoiceReport,InvoiceReportAdmin)

class PaymentReportAdmin (DefaultInline):
    change_list_template = "admin/account/account_action.html"
    list_display = ('id','status','amount')
    list_filter = ('status',('created_at', DateRangeFilter), 'invoices__area','invoices__lot','invoices__community')
    actions = ["export_as_csv"]
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(PaymentReport,PaymentReportAdmin)
class VisitReportAdmin (DefaultInline):
    change_list_template = "admin/account/account_action.html"
    list_display = ('id','status','visitor_car_plate','lot','area','created_at','updated_at')
    list_filter = (('created_at', DateRangeFilter),)
    actions = ["export_as_csv"]
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(VisitReport,VisitReportAdmin)