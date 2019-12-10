from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from residents.models import Request,ResidentLotThroughModel
class UserCreationForm(UserCreationForm):
    """
    A UserCreationForm with optional password inputs.
    """

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        # If one field gets autocompleted but not the other, our 'neither
        # password or both password' validation will be triggered.
        self.fields['password1'].widget.attrs['autocomplete'] = 'off'
        self.fields['password2'].widget.attrs['autocomplete'] = 'off'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = super(UserCreationForm, self).clean_password2()
        if bool(password1) ^ bool(password2):
            raise forms.ValidationError("Fill out both fields")
        return password2   

class EmailValidationForm(forms.Form):
    email = forms.EmailField()
    class Meta:
        fields = ('email',)
    def clean_email(self):
        email = self.cleaned_data.get('email', False)
        if email:
            exist = get_user_model().objects.filter(email=email,is_active= True)
            if exist:
                raise forms.ValidationError('Email address already activated.')
        else:
            raise forms.ValidationError('The email field is required.')
        return self.cleaned_data.get('email')
class ConfirmForm(forms.Form):
    agree = forms.BooleanField(label='I confirm that the information given in this form is true, complete and accurate.',required=True,)
    class Meta:
        fields = ('agree',)
class RequestForm(forms.ModelForm):
    class Meta: 
        model =  Request
        exclude = ('status',)
    def clean_confirm(self):
        if self.cleaned_data.get('confirm', False) is not True:
            raise forms.ValidationError("Please confirm the given information is true.")
        return self.cleaned_data.get('confirm')
    def clean_tou(self):
        if self.cleaned_data.get('tou', False) is not True:
            raise forms.ValidationError("Please accept the Privacy Policy.")
        return self.cleaned_data.get('confirm')
    def clean_email(self):
        email = self.cleaned_data.get('email', False)
        if email:
            exist = Request.objects.filter(email=email).filter(status="A").filter(status="R").filter(status="P")
            if exist:
                raise forms.ValidationError('Email address already registered.')
        else:
            raise forms.ValidationError('The email field is required.')
        return self.cleaned_data.get('email')
    def clean_lot(self):
        lot = self.cleaned_data.get('lot', False)
        if lot:
            exist = ResidentLotThroughModel.objects.filter(lot_id=lot)
            if exist:
                raise forms.ValidationError('This house already has an owner.')
        else:
            raise forms.ValidationError('The email field is required.')
        return self.cleaned_data.get('lot')