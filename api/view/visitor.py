from django.shortcuts import render,get_list_or_404,get_object_or_404
from rest_framework import generics,status,viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from api.serializer import visitor
from visitors.models import Track_Entry,Visitors,Entry_Schedule
from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_STRING, TYPE_ARRAY
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django.db.models import Q
class TrackEntryViewSet(viewsets.GenericViewSet):
    serializer_class = visitor.TrackEntryFormSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('status',)
    def get_queryset(self):
        queryset = Track_Entry.objects.filter(area=self.request.user.area)
        types = self.request.query_params.get('type', None)
        if types is not None and types == "WI":
            queryset = queryset.filter(Q(entry_type='W')|Q(entry_type='I'))
        if types is not None and types == "EMS":
            queryset = queryset.filter(Q(entry_type='E')|Q(entry_type='M')|Q(entry_type='S'))
        return queryset.order_by('-updated_at')
    def list (self,request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = visitor.TrackEntrySerializer(queryset,context={'request': request},many=True)
        return Response(serializer.data)
    def retrieve(self, request, pk=None):
        queryset = Track_Entry.objects.all()
        track = get_object_or_404(queryset, pk=pk)
        serializer = visitor.TrackEntrySerializer(track,context={'request': request})
        return Response(serializer.data)
    @swagger_auto_schema(request_body=visitor.TrackEntryFormSerializer,responses={201: Schema(type=TYPE_OBJECT,properties={'status':'success'})})
    def create(self,request,*args, **kwargs):
        serializer = self.serializer_class(data=request.data,context = {'request': self.request} )
        if serializer.is_valid():
            track = serializer.save()
            t = visitor.TrackEntrySerializer(track)
            response_data = {'status':'success','data':t.data}
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def update(self, request, pk=None):
        queryset = Track_Entry.objects.all()
        track = get_object_or_404(queryset, pk=pk)
        serializer = visitor.TrackUpdateStatusSerializer(track, data=request.data,context = {'request': self.request})
        if serializer.is_valid():
            serializer.save()
            response_data = {'status':'success'}
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VisitorViewSet(viewsets.GenericViewSet):
    serializer_class = visitor.VisitorSerializer
    def get_queryset(self):
        return Visitors.objects.filter(resident = self.request.user.resident,is_active=True)
    def list(self,request):
        queryset = Visitors.objects.filter(resident = self.request.user.resident,is_active=True).order_by('name')
        page = self.paginate_queryset(queryset)
        page = None
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        visitors = get_list_or_404(queryset,resident=self.request.user.resident.id)
        serializer = visitor.VisitorSerializer(visitors,context={'request': request},many=True)
        return Response(serializer.data)
    @swagger_auto_schema(request_body=visitor.VisitorSerializer,responses={201: visitor.VisitorSerializer()})
    def create(self,request,*args, **kwargs):
        serializer = self.serializer_class(data=request.data,context = {'request': self.request} )
        if serializer.is_valid():
            visitors = serializer.save()
            response_data = {'status':'success'}
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def retrieve(self, request, pk=None):
        queryset = Visitors.objects.all()
        visitors = get_object_or_404(queryset, pk=pk)
        serializer = visitor.VisitorSerializer(visitors,context={'request': request})
        return Response(serializer.data)
    def update(self, request, pk=None):
        queryset = Visitors.objects.all()
        visitors = get_object_or_404(queryset, pk=pk)
        serializer = visitor.VisitorSerializer(visitors, data=request.data,context = {'request': self.request})
        if serializer.is_valid():
            serializer.save()
            response_data = {'status':'success'}
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def destroy(self, request, pk=None):
        queryset = Visitors.objects.all()
        visitor = get_object_or_404(queryset, pk=pk)
        visitor.is_active=False
        visitor.save()
        response_data = {'status':'success'}
        return Response(response_data, status=status.HTTP_200_OK)
    @swagger_auto_schema(request_body=visitor.QRSerializer,responses={200: visitor.EntryScheduleSerializer()})
    @action(detail=False, methods=['post'],permission_classes=[AllowAny],serializer_class=visitor.QRSerializer)
    def check_qr(self, request):
        serializer =  visitor.QRSerializer(data=request.data)
        if serializer.is_valid():
            q = Entry_Schedule.objects.filter(is_active=True).all()
            areas = serializer.data.get('area_id',None)
            if areas != None:
                entry_schedule = get_object_or_404(q,qr_uuid=serializer.data['qr_uuid'],lot__street__area_id = areas)
            else:
                entry_schedule = get_object_or_404(q,qr_uuid=serializer.data['qr_uuid'])
            if entry_schedule:
                if entry_schedule.entry_type == 'E' and entry_schedule.start_date == datetime.now().date():
                    try:
                        tr = Track_Entry.objects.filter(entry_id=entry_schedule.id)
                        print(tr)
                    except Track_Entry.DoesNotExist:
                        tr = None
                    if tr == None or not tr:
                        return Response(visitor.EntryScheduleSerializer(entry_schedule).data,
                                status=status.HTTP_200_OK)
                else:
                    if entry_schedule.entry_type == 'M' and entry_schedule.start_date == datetime.now().date():
                        try:
                            tr = Track_Entry.objects.filter(entry_id=entry_schedule.id)
                        except Track_Entry.DoesNotExist:
                            tr = None
                        if tr == None or not tr:
                            return Response(visitor.EntryScheduleSerializer(entry_schedule).data,
                                status=status.HTTP_200_OK)
                        else:
                            for t in tr:
                                if t.status != 'AOS' and t.status != 'ROS':
                                    return Response({'status':'error'},
                                        status=status.HTTP_400_BAD_REQUEST)
                                else:
                                    return Response(visitor.EntryScheduleSerializer(entry_schedule).data,
                                        status=status.HTTP_200_OK)

                    else:
                        if entry_schedule.entry_type == 'S' and datetime.now().date()  >= entry_schedule.start_date and datetime.now().date() <=  entry_schedule.end_date :
                            try:
                                tr = Track_Entry.objects.filter(entry_id=entry_schedule.id)
                            except Track_Entry.DoesNotExist:
                                tr = None
                            if tr == None or not tr:
                                return Response(visitor.EntryScheduleSerializer(entry_schedule).data,
                                    status=status.HTTP_200_OK)
                            else:
                                for t in tr:
                                    if t.status != 'AOS' and t.status != 'ROS':
                                        return Response({'status':'error'},
                                            status=status.HTTP_400_BAD_REQUEST)
                            return Response(visitor.EntryScheduleSerializer(entry_schedule).data,status=status.HTTP_200_OK)
        return Response({'status':'error'}, status=status.HTTP_400_BAD_REQUEST)
    @action(detail=False, methods=['post'],permission_classes=[AllowAny],serializer_class=visitor.QRSerializer)
    def check_qr_exit(self, request):
        serializer =  visitor.QRSerializer(data=request.data)
        if serializer.is_valid():
            q = Entry_Schedule.objects.all()
            entry_schedule = get_object_or_404(q,qr_uuid=serializer.data['qr_uuid'])
            if entry_schedule:
                try:
                    tr = Track_Entry.objects.filter(entry_id=entry_schedule.id).order_by('-id')
                except Track_Entry.DoesNotExist:
                    tr = None
                if tr != None:
                    # for t in tr:
                    #     if t.status == 'AOS' :
                    #         return Response({'status':'error'},
                    #             status=status.HTTP_400_BAD_REQUEST)

                    return Response(visitor.TrackEntrySerializer(tr[0]).data,
                                status=status.HTTP_200_OK)
        return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

class EntryScheduleViewSet(viewsets.GenericViewSet):
    serializer_class = visitor.EntryScheduleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('entry_type',)
    def get_queryset(self):
        start_date = self.request.query_params.get('start_date', None)
        entry_type = self.request.query_params.get('entry_type', None)
        if entry_type:
            if start_date:
                return Entry_Schedule.objects.filter(resident = self.request.user.resident,start_date__lte = start_date,is_active=True).order_by('-id')
            else:
                return Entry_Schedule.objects.filter(resident = self.request.user.resident,is_active=True).order_by('-id')
        else:
            return Entry_Schedule.objects.filter(resident = self.request.user.resident, start_date__gt = start_date,is_active=True ).order_by('-id')
    @swagger_auto_schema(request_body=visitor.EntryScheduleSerializer,responses={201: visitor.EntryScheduleSerializer()})
    def create(self,request,*args, **kwargs):
        serializer = self.serializer_class(data=request.data,context = {'request': self.request} )
        if serializer.is_valid():
            entrySchedule = serializer.save()
            response_data = visitor.EntryScheduleSerializer(entrySchedule).data
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def retrieve(self, request, pk=None):
        queryset = Entry_Schedule.objects.all()
        visitors = get_object_or_404(queryset, pk=pk)
        serializer = visitor.EntryScheduleSerializer(visitors,context={'request': request})
        return Response(serializer.data)
    def list(self,request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        entry = get_list_or_404(queryset,resident=self.request.user.resident.id)
        serializer = visitor.EntryScheduleSerializer(entry,context={'request': request},many=True)
        return Response(serializer.data)
    def update(self, request, pk=None):
        queryset = Entry_Schedule.objects.all()
        entry = get_object_or_404(queryset, pk=pk)
        entry.is_active = False;
        entry.save();
        response_data = {'status':'success'}
        return Response(response_data, status=status.HTTP_200_OK)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def destroy(self, request, pk=None):
        queryset = Entry_Schedule.objects.all()
        entry = get_object_or_404(queryset, pk=pk)
        entry.is_active=False
        entry.save()
        response_data = {'status':'success'}
        return Response(response_data, status=status.HTTP_200_OK)
    @action(detail=False, methods=['get'],serializer_class=visitor.EntryScheduleSerializer)
    def sec_upcoming(self,request):
        queryset = Entry_Schedule.objects.filter(lot__street__area =self.request.user.area ,start_date__gt = datetime.now().date(),is_active=True).order_by('-id')
        serializer = visitor.EntryScheduleSerializer(queryset,context={'request': request},many=True)
        return Response(serializer.data)