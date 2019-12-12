from django.contrib import admin
# Register your models here.
from .models import Community,Area,Street,Lot,Resident,ResidentLotThroughModel,Request,Profile,RequestFamily
from ordered_model.admin import OrderedStackedInline, OrderedInlineModelAdminMixin
from jet.admin import CompactInline,DefaultInline
from django.contrib.auth import get_user_model
#from users.models import Profile
from django.template import loader,Context
from django.contrib.sites.shortcuts import get_current_site
from users.token import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
class AreaInline(admin.StackedInline):
     model = Area
     extra = 1

@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    inlines = [AreaInline]
    list_display = ('__str__',)

class StreetInline(CompactInline):
     model = Street
     extra = 1

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    inlines = [StreetInline]
    list_display = ('__str__','community')

class LotInline(CompactInline):
     model = Lot
     extra = 1

@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    inlines = [LotInline]
    list_display = ('__str__','community','area',)
    def community(self, obj):
        return obj.area.community

class ResidentInline(OrderedStackedInline):
    model = ResidentLotThroughModel
    fields = ('resident','lot','order','move_up_down_links',)
    readonly_fields = ('order','move_up_down_links',)
    max_num = 6
    extra = 1
    ordering = ('order',)

class LotAdmin(OrderedInlineModelAdminMixin, DefaultInline):
    search_fields = ('name', )
    inlines = [ResidentInline]
    list_display = ('__str__','community','area','is_lock')
    list_filter = ('street__area__community', )
    def community(self, obj):
        return obj.street.area.community
    def area(self, obj):
        return obj.street.area
class ResidentLotInline (CompactInline):
    model = ResidentLotThroughModel
    extra = 1

@admin.register(Resident)
class ResidentAdmin(DefaultInline):
    change_form_template = "admin/account/account_resent.html"
    search_fields = ('user__first_name','user__last_name','user__email','user__profile__phone_number' )
    fieldsets = [
        (None, {'fields':['user','default_lot']}),
    ]
    #inlines = (ResidentLotInline,)
    list_display = ('__str__','email','phone_number','default_house_lot')
    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields +('default_lot','user')
    def email(self, obj):
        return obj.user.email
    def phone_number(self, obj):
        return obj.user.profile.phone_number
    def default_house_lot(self,obj):
        return obj.default_lot
admin.site.register(Lot,LotAdmin)

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    search_fields = ('email', )
    list_display = ('email','first_name','last_name','status','community','area')
    list_filter = ('status', )
    # This will help you to disbale add functionality
    def get_queryset(self, request):
        qs = super(RequestAdmin, self).get_queryset(request)
        return qs.exclude(status__in=['A','R'])
    def has_add_permission(self, request):
        return False
    def get_readonly_fields(self, request, obj=None):
        '''
        Override to make certain fields readonly if this is a change request
        '''
        if obj is not None:
            rf = self.readonly_fields + ('email','first_name','last_name','phone_number','slip','community','area','street','lot','confirm','tou')
            if obj.status == 'A':
                rf = rf + ('status',)
            return rf
        return self.readonly_fields
    def save_model(self, request, obj, form, change):
        status = obj.status
        instance = super(RequestAdmin, self).save_model(request, obj, form, change)
        self.send_email(status,obj,request)
    def send_email(self,status,obj,request):
        if status == 'A':
            obj.is_active = False
            just_send = False
            try:
                user = get_user_model().objects.get(email=obj.email)
                r = Resident.objects.get(user_id=user.id)
            except (get_user_model().DoesNotExist, Resident.DoesNotExist) as e:
                just_send = True
                user = get_user_model().objects.create_user(
                    username = obj.email,
                    email=obj.email,
                    first_name=obj.first_name,
                    last_name=obj.last_name,
                    password=get_user_model().objects.make_random_password(),
                    is_active = False,
                    )
                p = Profile.objects.create(user=user,phone_number=obj.phone_number,community=obj.community)
                r = Resident.objects.create(user=user)
                current_site = get_current_site(request)
                mail_subject = 'Account Verification'
                message = loader.get_template(
                'emails/activateAccount.html').render(
                {
                    'name': user.first_name,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':account_activation_token.make_token(user),
                }
                )
                to_email = obj.email
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.content_subtype = 'html'
                email.send()
            rl = ResidentLotThroughModel.objects.create(resident=r,lot=obj.lot)
            ##Resend Activation Email
            if just_send == False and user.is_acitve == False and user.acc_is_activated == False:
                current_site = get_current_site(request)
                mail_subject = 'Account Verification'
                message = loader.get_template(
                'emails/activateAccount.html').render(
                {
                    'name': user.first_name,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':account_activation_token.make_token(user),
                }
                )
                to_email = obj.email
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.content_subtype = 'html'
                email.send()
            #obj.save()  
@admin.register(RequestFamily)
class RequestFamilyAdmin(admin.ModelAdmin):
    search_fields = ('email', )
    list_display = ('email','first_name','last_name','status','community','area','requestor')
    list_filter = ('status', )
    def get_queryset(self, request):
        qs = super(RequestFamilyAdmin, self).get_queryset(request)
        return qs.exclude(status__in=['A','R'])
    # This will help you to disbale add functionality
    def has_add_permission(self, request):
        return False
    def get_readonly_fields(self, request, obj=None):
        '''
        Override to make certain fields readonly if this is a change request
        '''
        if obj is not None:
            rf = self.readonly_fields + ('email','first_name','last_name','phone_number','community','area','street','lot','requestor')
            if obj.status == 'A':
                rf = rf + ('status',)
            return rf
        return self.readonly_fields
    def save_model(self, request, obj, form, change):
        status = obj.status
        instance = super(RequestFamilyAdmin, self).save_model(request, obj, form, change)
        self.send_email(status,obj,request)
    def send_email(self,status,obj,request):
        if status == 'A':
            obj.is_active = False
            try:
                user = get_user_model().objects.get(email=obj.email)
                r = Resident.objects.get(user_id=user.id)
            except (get_user_model().DoesNotExist, Resident.DoesNotExist) as e:
                user = get_user_model().objects.create_user(
                    username = obj.email,
                    email=obj.email,
                    first_name=obj.first_name,
                    last_name=obj.last_name,
                    password=get_user_model().objects.make_random_password(),
                    is_active = False,
                    )
                p = Profile.objects.create(user=user,phone_number=obj.phone_number,community=obj.community)
                r = Resident.objects.create(user=user)
                current_site = get_current_site(request)
                mail_subject = 'Account Verification'
                message = loader.get_template(
                'emails/activateAccount.html').render(
                {
                    'name': user.first_name,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':account_activation_token.make_token(user),
                }
                )
                to_email = obj.email
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.content_subtype = 'html'
                email.send()
            rl = ResidentLotThroughModel.objects.create(resident=r,lot=obj.lot)
            ##Resend Activation Email
            if just_send == False and user.is_acitve == False and user.acc_is_activated == False:
                current_site = get_current_site(request)
                mail_subject = 'Account Verification'
                message = loader.get_template(
                'emails/activateAccount.html').render(
                {
                    'name': user.first_name,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':account_activation_token.make_token(user),
                }
                )
                to_email = obj.email
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.content_subtype = 'html'
                email.send()
            #obj.save()  