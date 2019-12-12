from django.shortcuts import render,get_list_or_404,get_object_or_404
from django.contrib.auth import get_user_model
from residents.models import Lot,Community,Area,Street,Resident,ResidentLotThroughModel
from django.utils import timezone
from rest_framework import generics,status,viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from rest_framework_jwt.settings import api_settings
from drf_yasg.utils import swagger_auto_schema
from api.serializer import resident
from rest_framework.permissions import AllowAny
from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_STRING, TYPE_ARRAY
from rest_framework_jwt.serializers import (
    JSONWebTokenSerializer, RefreshJSONWebTokenSerializer,
    VerifyJSONWebTokenSerializer
)
from rest_framework_jwt.views import JSONWebTokenAPIView
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.template import loader,Context
from rest_framework.decorators import action
from rest_framework_jwt.views import JSONWebTokenAPIView
# Create your views here.
class ObtainJSONWebToken(JSONWebTokenAPIView):
    """
    API View that receives a POST with a user's username and password.

    Returns a JSON Web Token that can be used for authenticated requests.
    """
    serializer_class = resident.CustomJSONWebTokenSerializer

class ResidentViewSet(viewsets.GenericViewSet):
    """
    Get Resident Model.
    """
    @swagger_auto_schema(responses={200: resident.ResidentSerializer()})
    def list(self, request):
        queryset = Resident.objects.all()
        r = get_object_or_404(queryset, user_id=request.user.id)
        serializer = resident.ResidentSerializer(r,context = {'request': self.request})
        return Response(serializer.data)
    def update(self, request, pk=None):
        queryset = Resident.objects.all()
        r = get_object_or_404(queryset, user_id=pk)
        serializer = resident.ResidentSerializer(r, data=request.data,context = {'request': self.request},partial=True)
        if serializer.is_valid():
            serializer.save()
            response_data = {'status':'success'}
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @action(detail=False, methods=['post'],serializer_class=resident.defaultlotSerializer)
    def defaultProperty(self, request):
        queryset = Resident.objects.all()
        r = get_object_or_404(queryset, user_id=request.user.id)
        qs = Lot.objects.all()
        if(request.data['default_lot'] != '0'):
            req = get_object_or_404(qs, pk=request.data['default_lot'])
            r.default_lot = req
        else:
            r.default_lot = None
        r.save()
        response_data = {'status':'success'}
        return Response(response_data, status=status.HTTP_200_OK)
    @action(detail=False, methods=['post'],serializer_class=resident.RemoveLot)
    def removeLot(self,request):
        queryset = ResidentLotThroughModel.objects.all()
        if(request.data['user_id'] != '0' and request.data['lot_id'] != '0'):
            req = queryset.filter(resident_id = request.data['user_id'], lot_id = request.data['lot_id'])
            req.delete()
            rs = Resident.objects.get(pk=request.data['user_id'])
            if rs.user.is_active == False and rs.lot.count() == 0:
                rs.user.delete()
            response_data = {'status':'success'}
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @action(detail=False, methods=['post'],serializer_class=resident.FamilyOrderSerializer)
    def orderFamily(self, request):
        qs = ResidentLotThroughModel.objects.all()
        froms = get_object_or_404(qs, order=request.data['froms'],lot_id=request.data['lot'],resident_id=request.data['resident'])
        to  = get_object_or_404(qs, order=request.data['to'],lot_id=request.data['lot'],resident_id=request.data['resident_to'])
        froms.order = request.data['to']
        to.order = request.data['froms']
        froms.save()
        to.save()
        response_data = {'status':'success'}
        return Response(response_data, status=status.HTTP_200_OK)
    @action(detail=False, methods=['post'],serializer_class=resident.disablenotificationSerializer)
    def disableNotification(self, request):
        qs = ResidentLotThroughModel.objects.all()
        r = get_object_or_404(qs, resident_id=request.user.resident.id,lot_id=request.data['lot'])
        if(request.data['disable_notification'] == 'true'):
            r.disable_notification = True
        else:
            r.disable_notification = False
        r.save()
        response_data = {'status':'success'}
        return Response(response_data, status=status.HTTP_200_OK)
class RequestViewSet(viewsets.ViewSet):
    serializer_class = resident.RequestSerializer
    permission_classes = [AllowAny]
    @swagger_auto_schema(request_body=resident.RequestSerializer,responses={201: Schema(type=TYPE_OBJECT,request={'status':'success'})})
    def create(self,request,*args, **kwargs):
        serializer = self.serializer_class(data=request.data,context = {'request': self.request} )
        if serializer.is_valid():
            track = serializer.save()
            response_data = {'status':'success'}
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class RequestFamilyViewSet(viewsets.ViewSet):
    serializer_class = resident.RequestFamilySerializer
    @swagger_auto_schema(request_body=resident.RequestFamilySerializer,responses={201: Schema(type=TYPE_OBJECT,request={'status':'success'})})
    def create(self,request,*args, **kwargs):
        serializer = self.serializer_class(data=request.data,context = {'request': self.request} )
        if serializer.is_valid():
            try:
                user = get_user_model().objects.get(email=request.data['email'])
                resident = Resident.objects.get(user_id=user.id)
                resident_lot = ResidentLotThroughModel.objects.get(resident_id = resident.id, lot_id = request.data['lot'])
            except (get_user_model().DoesNotExist, Resident.DoesNotExist ,ResidentLotThroughModel.DoesNotExist) as e:
                track = serializer.save()
                response_data = {'status':'success'}
                return Response(response_data, status=status.HTTP_201_CREATED)
            return Response({'email':['user already exist']}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordRecoveryViewSet(viewsets.ViewSet):
    """
    Reset password endpoint.
    """
    serializer_class = resident.PasswordRecoverySerializer
    permission_classes = [AllowAny]
    @swagger_auto_schema(request_body=resident.PasswordRecoverySerializer,responses={200: RefreshJSONWebTokenSerializer()})
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = get_user_model().objects.get(email=request.data['email'])
            if(user.is_active == True):
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                current_site = get_current_site(request)
                mail_subject = 'Account Password Recovery'
                message = loader.get_template(
                'emails/forgotPassword.html').render(
                {
                    'name': user.first_name+' '+user.last_name,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':PasswordResetTokenGenerator().make_token(user),
                }
                )
                to_email = user.email
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.content_subtype = 'html'
                email.send()
                response_data = {
                    "token": token,
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                error = dict()
                error['email'] = 'Invalid email address.'
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordViewSet(viewsets.ViewSet):
    serializer_class = resident.ChangePasswordSerializer
    def create(self,request):
        serializer = self.serializer_class(data=request.data,context = {'request': self.request})
        if serializer.is_valid():
            user = request.user
            user.set_password(request.data['new_password'])
            user.save()
            response_data = {'status':'success'}
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PropertyViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    def get_queryset(self):
        return Community.objects.all()
    @action(detail=False, methods=['get'],permission_classes=[AllowAny],serializer_class=resident.CommunitySerializer)
    def getcommunity(self,request):
        queryset = Community.objects.all()
        serializer = resident.CommunitySerializer(queryset,context={'request': request},many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @action(detail=False, methods=['get'],permission_classes=[AllowAny],serializer_class=resident.AreaSerializer)
    def getarea(self,request):
        queryset = Area.objects.all()
        c_id = self.request.query_params.get('id', None)
        area = get_list_or_404(queryset,community_id = c_id )
        serializer = resident.AreaSerializer(area,context={'request': request},many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @action(detail=False, methods=['get'],permission_classes=[AllowAny],serializer_class=resident.StreetSerializer)
    def getstreet(self,request):
        queryset = Street.objects.all()
        c_id = self.request.query_params.get('id', None)
        area = get_list_or_404(queryset,area_id = c_id )
        serializer = resident.StreetSerializer(area,context={'request': request},many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @action(detail=False, methods=['get'],permission_classes=[AllowAny],serializer_class=resident.LotzSerializer)
    def getlot(self,request):
        queryset = Lot.objects.all()
        c_id = self.request.query_params.get('id', None)
        area = get_list_or_404(queryset,street_id = c_id )
        serializer = resident.LotzSerializer(area,context={'request': request},many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

custom_obtain_jwt_token = ObtainJSONWebToken.as_view()