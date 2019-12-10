from django.contrib import admin
from .models import BillType,BillSetting,Invoice,Payment
from jet.admin import CompactInline,DefaultInline
from jet.filters import DateRangeFilter

# Register your models here.

@admin.register(BillType)
class BillTypeAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_display = ('name',)
@admin.register(BillSetting)
class BillSettingAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_display = ('name','bill_type','amount','frequency','created_at')
class PaymentInline(admin.StackedInline):
     model = Payment
     extra = 1

@admin.register(Invoice)
class InvoiceAdmin(DefaultInline):
    search_fields = ('id','lot__name' )
    list_display = ('__str__','lot','area','amount','paid_amount','remainder','bill_type','paid','created_at','status')
    list_filter = ('is_paid','lot__name',('bill_date', DateRangeFilter),'bill_type','status' )
    inlines = [PaymentInline]
    def get_readonly_fields(self, request, obj=None):
        if obj: #This is the case when obj is already created i.e. it's an edit
            return ['name','community','lot','area','bill_date','bill_type','amount','remainder','paid','status']
        else:
            return []
    def paid(self, obj):
        if(obj.is_paid):
            return "Yes"
        else:
            return "No"
    def paid_amount(self,obj):
        return obj.amount - obj.remainder
    def get_form(self, request, obj=None, **kwargs):
        if obj:
            self.exclude = ('is_paid',)
        else:
            self.exclude = ('remainder','is_paid')
        form = super(InvoiceAdmin, self).get_form(request, obj, **kwargs)
        return form
