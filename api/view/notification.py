from django.shortcuts import render,get_list_or_404,get_object_or_404
from django.contrib.auth import get_user_model
from notification.models import Notification
from django.utils import timezone
from rest_framework import generics,status,viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from rest_framework_jwt.settings import api_settings
from drf_yasg.utils import swagger_auto_schema
from api.serializer import notification
from rest_framework.permissions import AllowAny
from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_STRING, TYPE_ARRAY
from rest_framework.decorators import action
# Create your views here.
class NotificationViewSet(viewsets.ViewSet):
    """
    Get Resident Model.
    """
    @swagger_auto_schema(responses={200: notification.NotificationSerializer()})
    def list(self, request):
        queryset = Notification.objects.all().order_by('-created_at')
        r = get_list_or_404(queryset, user_id=request.user.id)
        serializer = notification.NotificationSerializer(r,many=True)
        return Response(serializer.data)
    @action(detail=False, methods=['get'])
    def count(self, request):
        queryset = Notification.objects.filter(is_read=False)
        r = get_list_or_404(queryset, user_id=request.user.id)
        return Response({'count':len(r)},
                            status=status.HTTP_200_OK)
    def update(self, request, pk=None):
        response_data = {'status':'success'}
        newPk = pk[:2]
        if(newPk  == 'id'):
            Notification.objects.filter(object_id=pk[2:]).update(is_read = 1)
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            queryset = Notification.objects.all()
            track = get_object_or_404(queryset, pk=pk)
            serializer = notification.NotificationSerializer(track, data=request.data,context = {'request': self.request},partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @action(detail=False, methods=['delete'])      
    def destroyAll(self, request):
        queryset = Notification.objects.all()
        r = get_list_or_404(queryset, user_id=request.user.id)
        for a in r:
            a.delete()
        response_data = {'status':'success'}
        return Response(response_data, status=status.HTTP_200_OK)
    def destroy(self, request, pk=None):
        queryset = Notification.objects.all()
        notification = get_object_or_404(queryset, pk=pk)
        notification.delete()
        response_data = {'status':'success'}
        return Response(response_data, status=status.HTTP_200_OK)