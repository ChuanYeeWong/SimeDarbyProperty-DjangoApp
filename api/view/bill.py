from django.shortcuts import render,get_list_or_404,get_object_or_404
from django.contrib.auth import get_user_model
from announcements.models import Announcement
from django.utils import timezone
from rest_framework import generics,status,viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from api.serializer import bill
from django_filters.rest_framework import DjangoFilterBackend
from billings.models import Invoice,Payment
from rest_framework.decorators import action
class BillingViewSet(viewsets.GenericViewSet):
    serializer_class = bill.InvoiceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('status','lot')
    def get_queryset(self):
        lot = self.request.query_params.get('lot', None)
        finish = self.request.query_params.get('finish', None)
        queryset = Invoice.objects.filter(lot=lot)
        if finish:
            queryset = queryset.exclude(status__in = ['S','V']).order_by('-created_at')
        return queryset
    def list (self,request):
        queryset = self.filter_queryset(self.get_queryset());
        limit = self.request.query_params.get('limits', None)
        if(limit):
            queryset = queryset[:int(limit)]
        serializer = bill.InvoiceSerializer(queryset,context={'request': request},many=True)
        return Response(serializer.data)
    def retrieve(self, request, pk=None):
        queryset = Invoice.objects.all()
        track = get_object_or_404(queryset, pk=pk)
        serializer = bill.InvoiceSerializer(track,context={'request': request})
        return Response(serializer.data)
    @action(detail=False, methods=['post'],serializer_class=bill.PaySerializer)
    def pay(self, request):
        serializer = self.serializer_class(data=request.data,context = {'request': self.request} )
        if serializer.is_valid():
            track = serializer.save()
            response_data = {'status':'success'}
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)