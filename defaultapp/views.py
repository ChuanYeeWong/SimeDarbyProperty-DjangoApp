from django.shortcuts import render
from django.core.management import execute_from_command_line
from django.http import HttpResponse
import os 
# Create your views here.
def default_view(request):
    return render(request,'users/default.html')

def auto_update_annoucement(request):
    #a = execute_from_command_line(["manage.py", "update_announcements"])
    a = os.system("/home/env/bin/python /home/DjangoApp/manage.py update_announcements")
    return HttpResponse(a)
def auto_family(request):  
    a = os.system("/home/env/bin/python /home/DjangoApp/manage.py update_family")
    return HttpResponse(a)