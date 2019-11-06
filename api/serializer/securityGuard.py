import jwt
from django.contrib.auth import get_user_model
from rest_framework import serializers
from residents.models import Lot,Community,Area,Street,Resident,ResidentLotThroughModel,Profile
from rest_framework_jwt.compat import Serializer
from ivms.models import IPCamera,Boomgate
from security_guards.models import Security,ReasonSetting,PassNumber,DeviceNumber,BoomgateLog
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_jwt.compat import PasswordField
from rest_framework_jwt.settings import api_settings
from api.utils import jwt_payload_handler, jwt_encode_handler, jwt_decode_handler,jwt_get_username_from_payload_handler
from django.utils.translation import ugettext as _
from .resident import UserSerializer,StreetSerializer
class LotOnlySerializer(serializers.ModelSerializer):
    has_resident = serializers.SerializerMethodField()
    def get_has_resident(self,obj):
        resident = obj.resident_set.count()
        if resident == 0:
            return False
        return True
    class Meta:
        model = Lot
        fields = (
            'id',
            'is_lock',
            'has_resident',
            'name',
        )
class StreetLotSerializer(serializers.ModelSerializer):
    lot_set =LotOnlySerializer(many=True,read_only=True)
    class Meta:
        model = Street
        fields = (
            'id',
            'name',
            'lot_set',
            
        )
class BoomgateLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoomgateLog
        fields = (
            'type',
            'reason',
        )
class IPCamSerializer(serializers.ModelSerializer):
    class Meta:
        model = IPCamera
        fields = (
            'url', 
            'type',
        )
class BoomgateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boomgate
        fields = (
            'url', 
            'type',
        )
class ReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReasonSetting
        fields = (
            'id',
            'reason',
        )
class SecuritySerializer(serializers.ModelSerializer):
    community_name = serializers.CharField(source='community.name')
    area_name = serializers.CharField(source='area.name')
    class Meta:
        model = Security
        fields=('id','username','first_name','last_name','status','community_name','area_name','area')
        read_only_fields = ('__all__',)
class PassNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassNumber
        fields=('id','pass_no',)
        read_only_fields = ('__all__',)
class DeviceNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceNumber
        fields=('id','device_no',)
        read_only_fields = ('__all__',)
class ResidentUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Resident
        fields=(
            'user',
        )
class ResidentLotThroughModelSerializer(serializers.ModelSerializer):
    resident = ResidentUserSerializer()
    class Meta:
        model = ResidentLotThroughModel
        fields=(
            'resident',
            'order',
        )
class GetPrimarySerializer(serializers.ModelSerializer):
    street = StreetSerializer()
    resident = serializers.SerializerMethodField()
    def get_resident(self, obj):
        res = ResidentLotThroughModel.objects.filter(order=0,lot=obj)
        serializer = ResidentLotThroughModelSerializer(instance=res,many=True)
        return serializer.data
    class Meta:
        model = Lot
        fields = (
            'street',
            'name',
            'resident',
        )
        ordering = ['-id']
class SecurityWebTokenSerializer(Serializer):
    """
    Serializer class used to validate a username and password.
    'username' is identified by the custom UserModel.USERNAME_FIELD.
    Returns a JSON Web Token that can be used to authenticate later calls.
    """
    def __init__(self, *args, **kwargs):
        """
        Dynamically add the USERNAME_FIELD to self.fields.
        """
        super(SecurityWebTokenSerializer, self).__init__(*args, **kwargs)

        self.fields['username'] = serializers.CharField()
        self.fields['password'] = PasswordField(write_only=True)


    def validate(self, attrs):
        credentials = {
            'username': attrs.get('username'),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            try:
                user = Security.objects.get(username=credentials['username'])
            except Security.DoesNotExist:
                user = None
            if user:
                password = credentials['password'] + user.salt
                if check_password(password ,user.password):
                    if user.status == 'I':
                        msg = 'User account is disabled.'
                        raise serializers.ValidationError(msg)

                    payload = jwt_payload_handler(user)

                    return {
                        'token': jwt_encode_handler(payload),
                        'user': user
                    }
                else:
                    msg = 'Unable to log in with provided credentials.'
                    raise serializers.ValidationError(msg)
            else:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg)
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg)

class SVerificationBaseSerializer(Serializer):
    """
    Abstract serializer used for verifying and refreshing JWTs.
    """
    token = serializers.CharField()

    def validate(self, attrs):
        msg = 'Please define a validate method.'
        raise NotImplementedError(msg)

    def _check_payload(self, token):
        # Check payload valid (based off of JSONWebTokenAuthentication,
        # may want to refactor)
        try:
            payload = jwt_decode_handler(token)
        except jwt.ExpiredSignature:
            msg = _('Signature has expired.')
            raise serializers.ValidationError(msg)
        except jwt.DecodeError:
            msg = _('Error decoding signature.')
            raise serializers.ValidationError(msg)

        return payload

    def _check_user(self, payload):
        username = jwt_get_username_from_payload_handler(payload)

        if not username:
            msg = _('Invalid payload.')
            raise serializers.ValidationError(msg)

        # Make sure user exists
        try:
            user = Security.objects.get(username=username)
        except Security.DoesNotExist:
            msg = _("User doesn't exist.")
            raise serializers.ValidationError(msg)

        if not user.status != "I":
            msg = _('User account is disabled.')
            raise serializers.ValidationError(msg)

        return user

class SVerifyJSONWebTokenSerializer(SVerificationBaseSerializer):
    """
    Check the veracity of an access token.
    """

    def validate(self, attrs):
        token = attrs['token']

        payload = self._check_payload(token=token)
        user = self._check_user(payload=payload)

        return {
            'token': token,
            'user': user
        }
