"""Integrate with admin module."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from .models import User
from residents.models import Profile
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget, PhoneNumberPrefixWidget
from jet.admin import DefaultUserInline
from .forms import UserCreationForm
from django.template import loader,Context
from django.contrib.sites.shortcuts import get_current_site
from .token import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
class UserInline(admin.StackedInline):
    model = Profile
    can_delete = False
    formfield_overrides = {
        PhoneNumberField: {'widget': PhoneNumberPrefixWidget,'initial':'+60'},
    }

@admin.register(User)
class UserAdmin(DefaultUserInline):
    """Define admin model for custom User model with no email field."""
    add_form = UserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name','last_name','is_staff'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff','is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    inlines = (UserInline,)
    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets

        if request.user.is_superuser:
            perm_fields = ('is_active', 'is_staff', 'is_superuser',
                           'groups', 'user_permissions')
        else:
            # modify these to suit the fields you want your
            # staff user to be able to edit
            perm_fields = ('is_active', 'is_staff')

        return [(None, {'fields': ('email', 'password','first_name','last_name')}),
                (_('Permissions'), {'fields': perm_fields})]
    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(is_superuser=False)
        return qs
    def save_model(self, request, obj, form, change):
        is_created = obj.pk is None
        instance = super(UserAdmin, self).save_model(request, obj, form, change)
        self.send_email(is_created,obj,request)
    def send_email(self,create,obj,request):
        if create:
            current_site = get_current_site(request)
            mail_subject = 'Account Verification'
            message = loader.get_template(
            'emails/activateAccount.html').render(
            {
                'name': obj.first_name,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(obj.pk)),
                'token':account_activation_token.make_token(obj),
            }
            )
            to_email = obj.email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.content_subtype = 'html'
            email.send()

            obj.password  =  get_user_model().objects.make_random_password()
            obj.save()  