from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token import account_activation_token
from django.contrib.auth import get_user_model
from .forms import EmailValidationForm,ConfirmForm,RequestForm
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from residents.models import Request
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        form = EmailValidationForm()
        if request.method == 'POST':
            f = EmailValidationForm(request.POST)
            if f.is_valid():
                if f.cleaned_data['email'] == user.email:
                    return redirect('user-terms',uidb64=uidb64,token=token)
            else:
                form = f
        return render(request, 'users/emailValidation.html', {'form': form})

    else:
        return render(request, 'users/invalid.html')


def confirm_terms(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        form = ConfirmForm()
        if request.method == 'POST':
            f = ConfirmForm(request.POST)
            if f.is_valid():
                user.is_active = True
                user.save()
                tkn = PasswordResetTokenGenerator().make_token(user)
                return redirect('password_reset_confirm',uidb64=uidb64,token=tkn)
            else:
                form = f
        return render(request, 'users/tou.html', {'form': form, 'user':user})

    else:
        return HttpResponse('Activation link is invalid!')
        

@csrf_exempt
@xframe_options_exempt
def request_resident(request):
    if request.method == "POST":
        form = RequestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('register_complete')
    else:
        form = RequestForm()
    return render(request,'users/register.html',{'form':form,})
@xframe_options_exempt
def request_complete(request):
    return render(request,'users/register_complete.html')