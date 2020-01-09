from django.contrib.auth import get_user_model
from rest_framework import serializers
from residents.models import Lot,Community,Area,Street,Resident,ResidentLotThroughModel,Profile,Request,RequestFamily
from django.contrib.auth.hashers import check_password
import django.contrib.auth.password_validation as validators
from django.core import exceptions
import jwt

from calendar import timegm
from datetime import datetime, timedelta

from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext as _
from rest_framework import serializers
from rest_framework_jwt.compat import Serializer

from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.compat import get_username_field, PasswordField
from django.contrib.auth.signals import user_logged_in

from push_notifications.models import GCMDevice
User = get_user_model()
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER
#import django.contrib.auth.password_validation as validators
#user module serializer
class CustomJSONWebTokenSerializer(Serializer):
    """
    Serializer class used to validate a username and password.

    'username' is identified by the custom UserModel.USERNAME_FIELD.

    Returns a JSON Web Token that can be used to authenticate later calls.
    """
    def __init__(self, *args, **kwargs):
        """
        Dynamically add the USERNAME_FIELD to self.fields.
        """
        super(CustomJSONWebTokenSerializer, self).__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = PasswordField(write_only=True)
        self.fields['reg_id'] = serializers.CharField(required=False) 
        self.fields['device_id'] = serializers.CharField(required=False) 
    @property
    def username_field(self):
        return get_username_field()

    def validate(self, attrs):
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password'),
            'request':self.context.get('request')
        }

        if all(credentials.values()):
            user = authenticate(**credentials)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)

                if attrs.get('reg_id') != None:
                    try:
                        gcm = GCMDevice.objects.get(registration_id=attrs.get('reg_id'))
                    except GCMDevice.DoesNotExist:
                        gcm = GCMDevice.objects.create(user=user,registration_id=attrs.get('reg_id'),device_id=attrs.get('device_id'),cloud_message_type='FCM')

                payload = jwt_payload_handler(user)
                user_logged_in.send(sender=user.__class__, request=self.context.get('request'), user=user)
                return {
                    'token': jwt_encode_handler(payload),
                    'user': user
                }
            else:

                msg = _('Unable to log in with provided credentials.')
                #raise serializers.ValidationError(user)
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "{username_field}" and "password".')
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'phone_number',
        )
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = get_user_model()
        fields = (
            'id', 
            'first_name',
            'last_name', 
            'email', 
            'is_active',
            'profile',
        )
class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = (
            'id',
            'name',
        )
class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = (
            'id',
            'name',
            'thumbnail',
        )
class StreetSerializer(serializers.ModelSerializer):
    area = AreaSerializer()
    class Meta:
        model = Street
        fields = (
            'id',
            'name',
            'area',
            
        )
class LotzSerializer(serializers.ModelSerializer):
    street = StreetSerializer()
    class Meta:
        model = Lot
        fields = (
            'id',
            'name',
            'street',
            
        )
class ResidentFamSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Resident
        fields=(
            'user',
        )
class ResidentLotThroughModelSerializer(serializers.ModelSerializer):
    resident = ResidentFamSerializer()
    class Meta:
        model = ResidentLotThroughModel
        fields =(
            'resident',
            'disable_notification',
            'order',
            'resident_id',
        )
class RequestFamilyLotSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestFamily
        fields=(
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'status',
        )
class LotSerializer(serializers.ModelSerializer):
    street = StreetSerializer()
    residentlotthroughmodel_set = ResidentLotThroughModelSerializer(many=True)
    requestfamily = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    is_default = serializers.SerializerMethodField()
    is_notify = serializers.SerializerMethodField()
    def get_is_owner(self, obj):
        res = ResidentLotThroughModel.objects.filter(lot_id=obj.id, resident_id=self.context['request'].user.resident.id )[0]
        if res.order == 0:
            return True
        return False
    def get_is_default(self, obj):
        res = Resident.objects.get(pk=self.context['request'].user.resident.id)
        if res.default_lot:
            if res.default_lot.id == obj.id:
                return True
        return False
    def get_requestfamily(self,obj):
        try:
            res = RequestFamily.objects.filter(lot_id = obj.id).exclude(status = 'A').exclude(status = 'R')
        except RequestFamily.DoesNotExist:
            return None
        return RequestFamilyLotSerializer(res,many=True).data
    def get_is_notify(self,obj):
        res = ResidentLotThroughModel.objects.filter(lot_id=obj.id, resident_id=self.context['request'].user.resident.id )[0]
        if res.disable_notification == True:
            return True
        return False
    class Meta:
        model = Lot
        fields = (
            'id',
            'street',
            'is_lock',
            'residentlotthroughmodel_set',
            'requestfamily',
            'name',
            'is_owner',
            'is_default',
            'is_notify',
        )
class RemoveLot(serializers.Serializer):
    user_id = serializers.IntegerField()
    lot_id = serializers.IntegerField()
class FamilyOrderSerializer(serializers.Serializer):
    froms = serializers.IntegerField()
    to = serializers.IntegerField()
    lot = serializers.IntegerField()
    resident = serializers.IntegerField()
    resident_to = serializers.IntegerField()
class LotSecSerializer(serializers.ModelSerializer):
    street = StreetSerializer()
    residentlotthroughmodel_set = ResidentLotThroughModelSerializer(many=True)
    requestfamily_set = RequestFamilyLotSerializer(many=True)
    class Meta:
        model = Lot
        fields = (
            'id',
            'street',
            'is_lock',
            'residentlotthroughmodel_set',
            'requestfamily_set',
            'name',
        )
class ResidentSecSerializer(serializers.ModelSerializer):
    lot = LotSecSerializer(many=True)
    user = UserSerializer()
    class Meta:
        model = Resident
        fields=(
            'id',
            'user',
            'lot',
            'default_lot',
        )
class defaultlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resident
        fields=(
            'lot',
            'default_lot',
        )
class disablenotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResidentLotThroughModel
        fields =(
            'lot',
            'resident',
            'disable_notification',
        )
class ResidentSerializer(serializers.ModelSerializer):
    lot = LotSerializer(many=True)
    user = UserSerializer()
    is_lock_down = serializers.SerializerMethodField()
    def get_is_lock_down(self,obj):
        res = ResidentLotThroughModel.objects.filter(resident_id=self.context['request'].user.resident.id )
        for l in res:
            if l.lot.is_lock == False:
                return False
        return True
    class Meta:
        model = Resident
        fields=(
            'user',
            'lot',
            'default_lot',
            'is_lock_down',
        )
class RequestSerializer(serializers.ModelSerializer):
    confirm =  serializers.BooleanField(default=False)
    tou =  serializers.BooleanField(default=False)
    class Meta:
        model = Request
        fields=(
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'status',
            'slip',
            'community',
            'area',
            'street',
            'lot',
            'confirm', 
            'tou',
        )
    def validate_confirm(self, value):
        if value is not True:
            raise serializers.ValidationError("This field is required")
        return value
    def validate_tou(self, value):
        if value is not True:
            raise serializers.ValidationError("This field is required")
        return value
class RequestFamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestFamily
        fields=(
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'lot',
        )
    def get_current_user(self):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            return request.user
        return None
    def create(self,validated_data):
        user =  self.get_current_user()
        lot = Lot.objects.get(id=int(validated_data['lot'].id))
        requestFamily = RequestFamily.objects.create(
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            phone_number = validated_data['phone_number'],
            community =  lot.street.area.community,
            area = lot.street.area,
            street = lot.street,
            lot = lot,
            requestor = user.resident
        )
        return requestFamily
class PasswordRecoverySerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True)
    class Meta:
        model = get_user_model()
        fields = (
            'email', 
        )
    def validate(self, validated_data):
        """
        Check for existing E-mail
        """
        email = validated_data['email']
        try:
           self.user = get_user_model().objects.get(email=email)
        except exceptions.ObjectDoesNotExist:
            raise serializers.ValidationError('email does not exist')
        return validated_data
class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True,style={'input_type': 'password'})
    new_password = serializers.CharField(required=True,style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True,style={'input_type': 'password'})
    class Meta:
        model = get_user_model()
        fields = (
            'password',
            'new_password',
            'confirm_password', 
        )
    def get_current_user(self):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            return request.user
        return None
    def validate(self, validated_data):
        """
        Check for existing E-mail
        """
        password = validated_data['password']
        new_password = validated_data['new_password']
        confirm_password = validated_data['confirm_password']
        user =  self.get_current_user()
        error = dict()
        if check_password(password,user.password) is False:
            error['password'] = 'Invalid password.'
            raise serializers.ValidationError(error)
        if new_password != confirm_password:
            error['new_password'] = 'New password is not the same.'
            raise serializers.ValidationError(error)
        try:
             # validate the password and catch the exception
             validators.validate_password(password=new_password, user=user)

         # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            error['new_password']=list(e.messages)
            raise serializers.ValidationError(error)

        return validated_data