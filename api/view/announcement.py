from django.shortcuts import render,get_list_or_404,get_object_or_404
from django.contrib.auth import get_user_model
from announcements.models import Announcement
from django.utils import timezone
from rest_framework import generics,status,viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from api.serializer import announcement
from django_filters.rest_framework import DjangoFilterBackend
from residents.models import Resident,Area,Street
class AnnouncementViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Get Announcement Model.

    retrieve: 
    List All Announcements.

    """
    serializer_class = announcement.AnnouncementSerializer
    def get_queryset(self):
        queryset = Resident.objects.all()
        r = get_object_or_404(queryset, user_id=self.request.user.id)
        street = Street.objects.filter(lot__in=r.lot.all())
        area = Area.objects.filter(street__in=street)
        queryset = Announcement.objects.all().filter(publish_datetime__lte = timezone.now(),area__in=area).order_by('-publish_datetime')
        limits = self.request.query_params.get('limits', None)
        if limits is not None and limits != '0':
            queryset = queryset[:int(limits)]
        return queryset
