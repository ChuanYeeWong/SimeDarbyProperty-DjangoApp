from django.shortcuts import render,get_list_or_404
from django.contrib.auth import get_user_model
from residents.models import Lot,Community,Area,Street,Resident
from ivms.models import IPCamera,Boomgate
from django.utils import timezone
from rest_framework import generics,viewsets,status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.views import JSONWebTokenAPIView
from api.utils import jwt_response_payload_handler
from api.jwt_login import sjwt_response_payload_handler
from datetime import datetime
from rest_framework_jwt.settings import api_settings
from security_guards.models import ReasonSetting,PassNumber,DeviceNumber,Security,BoomgateLog
from drf_yasg.utils import swagger_auto_schema
from api.serializer import securityGuard,resident
class GetPrimaryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Get Primary User By House Lot.
    """
    queryset = Lot.objects.all()
    serializer_class = securityGuard.GetPrimarySerializer
class SJSONWebTokenAPIView(APIView):
    """
    Base API View that various JWT interactions inherit from.
    """
    permission_classes = ()
    authentication_classes = ()

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'view': self,
        }

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.
        You may want to override this if you need to provide different
        serializations depending on the incoming request.
        (Eg. admins get full serialization, others get basic serialization)
        """
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__)
        return self.serializer_class

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = sjwt_response_payload_handler(token, user, request)
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SecurityLogin(SJSONWebTokenAPIView):
    serializer_class = securityGuard.SecurityWebTokenSerializer

class SVerifyJSONWebToken(SJSONWebTokenAPIView):
    """
    API View that checks the veracity of a token, returning the token if it
    is valid.
    """
    serializer_class = securityGuard.SVerifyJSONWebTokenSerializer

class PassNumberViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PassNumber.objects.all()
    serializer_class = securityGuard.PassNumberSerializer
    def get_queryset(self):
        return PassNumber.objects.filter(area=self.request.user.area)
class DeviceNumberViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DeviceNumber.objects.all()
    serializer_class = securityGuard.DeviceNumberSerializer
    def get_queryset(self):
        return DeviceNumber.objects.filter(area=self.request.user.area)
class SecStreetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Street.objects.all()
    serializer_class = securityGuard.StreetLotSerializer
    def get_queryset(self):
        return Street.objects.filter(area=self.request.user.area)
class ReasonViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Get Resident Model.
    """
    queryset = ReasonSetting.objects.all()
    serializer_class = securityGuard.ReasonSerializer

class SecResidentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Resident.objects.all()
    serializer_class = resident.ResidentSecSerializer
    def get_queryset(self):
        return Resident.objects.filter(lot__street__area = self.request.user.area, lot__street__id = self.request.query_params.get('street'), lot__id = self.request.query_params.get('lot'))
class SecIPCamViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = IPCamera.objects.all()
    serializer_class = securityGuard.IPCamSerializer
    def get_queryset(self):
        return IPCamera.objects.filter(area=self.request.user.area)
class BoomgateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Boomgate.objects.all()
    serializer_class = securityGuard.BoomgateSerializer
    pagination_class = None
    def get_queryset(self):
        return Boomgate.objects.filter(area=self.request.user.area)
class SecBoomgateLogViewSet(viewsets.ViewSet):
    def create(self, request):
        bg = BoomgateLog()
        bg.type = request.data['type']
        bg.reason_id = request.data['reason']
        bg.security_guard = request.user
        bg.save()
        serializer = securityGuard.BoomgateLogSerializer(bg)
        return Response(serializer.data)