from django.contrib import admin
from .models import Security,ReasonSetting,PassNumber,DeviceNumber
from django.contrib.auth.hashers import make_password
import crypt
from django import forms
# Register your models here.
class SecurityForm(forms.ModelForm):

    class Meta:
        model = Security
        exclude = ['salt']

@admin.register(Security)
class SecurityAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_display = ('first_name','last_name','community','area')
    form = SecurityForm
    def save_model(self, request, obj, form, change):
        obj.salt = crypt.mksalt(crypt.METHOD_SHA512)
        p = obj.password
        obj.password = make_password(p + obj.salt)
        instance = super(SecurityAdmin, self).save_model(request, obj, form, change)
        obj.save()
@admin.register(ReasonSetting)
class ReasonSettingAdmin(admin.ModelAdmin):
    search_fields = ('name', )
@admin.register(PassNumber)
class ReasonSettingAdmin(admin.ModelAdmin):
    pass_no = ('pass_no', )
    list_display = ('pass_no','community','area',)
    list_filter = ('community', 'area',)
@admin.register(DeviceNumber)
class ReasonSettingAdmin(admin.ModelAdmin):
    search_fields = ('device_no', )
    list_display = ('device_no','community','area',)
    list_filter = ('community', 'area',)
