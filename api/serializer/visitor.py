from rest_framework import serializers
from rest_framework_jwt.compat import Serializer
from visitors.models import Visitors,Entry_Schedule,Track_Entry
from .resident import AreaSerializer,StreetSerializer,LotSecSerializer,ResidentSerializer,ProfileSerializer
from residents.models import Resident,Lot
from .securityGuard import DeviceNumberSerializer,PassNumberSerializer
import uuid
class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Visitors
        fields=(
            'id',
            'name',
            'car_plate',
            'phone_number',
        )
    def create(self,validated_data):
        user = self.context['request'].user
        visitor = Visitors.objects.create(
            name = validated_data['name'],
            car_plate = validated_data['car_plate'],
            phone_number = validated_data['phone_number'],
            resident = user.resident
        )
        return visitor
class TrackEntryFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track_Entry
        fields=(
            'driver_image',
            'entry_car_plate_image',
            'identity_image',
            'exit_car_plate_image',
            'status',
            'entry_type',
            'visitor_name',
            'visitor_car_plate',
            'visitor_phone_number',
            'visitor',
            'with_vehicle',
            'entry',
            'lot',
            'area',
            'street',
            'community',
            'resident',
            'passNumber',
            'deviceNumber',
            'reason',
        )
    def get_current_user(self):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            return request.user
        return None
    def create(self,validated_data):
        user =  self.get_current_user()
        track = Track_Entry.objects.create(
            driver_image = validated_data['driver_image'],
            entry_car_plate_image = validated_data['entry_car_plate_image'],
            identity_image = validated_data['identity_image'],
            exit_car_plate_image = validated_data.get('exit_car_plate_image', None),
            status = validated_data['status'],
            entry_type = validated_data['entry_type'],
            visitor_car_plate = validated_data['visitor_car_plate'],
            area = validated_data.get('area',getattr(user,'area',None)),
            visitor_name = validated_data.get('visitor_name',None),
            community = validated_data.get('community',getattr(user,'community',None)),
            street = validated_data.get('street', None),
            with_vehicle = validated_data.get('with_vehicle', None),
            lot = validated_data.get('lot', None),
            resident = validated_data.get('resident', None),
            entry = validated_data.get('entry', None),
            passNumber = validated_data.get('passNumber', None),
            deviceNumber = validated_data.get('deviceNumber', None),
            reason = validated_data.get('reason', None),
        )
        return track

class TrackEntrySerializer(serializers.ModelSerializer):
    lot = LotSecSerializer()
    tracker_id = serializers.IntegerField(source='id')
    phone_number = serializers.SerializerMethodField()
    resident_name = serializers.SerializerMethodField()
    deviceNumber = DeviceNumberSerializer()
    passNumber = PassNumberSerializer()
    def get_phone_number(self, obj):
        if obj.resident :
            res = Resident.objects.get(id=obj.resident.id)
            return str(res.user.profile.phone_number)
        else:
            return None
    def get_resident_name(self, obj):
        if obj.resident :
            res = Resident.objects.get(id=obj.resident.id)
            return res.user.first_name +" "+res.user.last_name
        else:
            return None
    class Meta:
        model = Track_Entry
        fields=(
            'tracker_id',
            'driver_image',
            'entry_car_plate_image',
            'identity_image',
            'exit_car_plate_image',
            'status',
            'entry_type',
            'visitor_name',
            'visitor_car_plate',
            'visitor_phone_number',
            'visitor',
            'with_vehicle',
            'created_at',
            'updated_at',
            'entry',
            'lot',
            'community',
            'resident',
            'phone_number',
            'passNumber',
            'deviceNumber',
            'reason',
            'resident_name',
        )
class TrackUpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track_Entry
        fields=(
            'status',
            'exit_car_plate_image',
        )
class QRSerializer(serializers.ModelSerializer):
    area_id = serializers.IntegerField(required=False)
    class Meta:
        model = Entry_Schedule
        fields = (
            'qr_uuid',
            'area_id',
        )
      

class EntryScheduleSerializer(serializers.ModelSerializer):
    area_name = serializers.SerializerMethodField()
    street_name = serializers.SerializerMethodField()
    community = serializers.SerializerMethodField()
    area = serializers.SerializerMethodField()
    street = serializers.SerializerMethodField()
    lot_name = serializers.SerializerMethodField()
    def get_area_name(self, obj):
        if obj.resident :
            res = Lot.objects.get(id=obj.lot.id)
            return res.street.area.name
        else:
            return None
    def get_lot_name(self,obj):
        if obj.resident :
            res = Lot.objects.get(id=obj.lot.id)
            return res.name
        else:
            return None
    def get_street_name(self, obj):
        if obj.resident :
            res = Lot.objects.get(id=obj.lot.id)
            return res.street.name
        else:
            return None
    def get_area(self, obj):
        if obj.resident :
            res = Lot.objects.get(id=obj.lot.id)
            return res.street.area.id
        else:
            return None
    def get_street(self, obj):
        if obj.resident :
            res = Lot.objects.get(id=obj.lot.id)
            return res.street.id
        else:
            return None
    def get_community(self, obj):
        if obj.resident :
            res = Lot.objects.get(id=obj.lot.id)
            return res.street.area.community.id
        else:
            return None
    class Meta:
        model = Entry_Schedule
        fields=(
            'id',
            'lot',
            'start_date',
            'end_date',
            'is_notify',
            'qr_uuid',
            'entry_type',
            'days',
            'visitor_name',
            'visitor_car_plate',
            'visitor_phone_number',
            'visitor',
            'resident',
            'area_name',
            'street_name',
            'community',
            'lot_name',
            'area',
            'street',
        )
        read_only_fields = ('qr_uuid','resident','id')
    def create(self,validated_data):
        user = self.context['request'].user
        entry_schedule = Entry_Schedule.objects.create(
            lot = validated_data['lot'],
            is_notify = validated_data['is_notify'],
            entry_type = validated_data['entry_type'],
            visitor_name = validated_data['visitor_name'],
            visitor_car_plate = validated_data['visitor_car_plate'],
            visitor_phone_number = validated_data['visitor_phone_number'],
            start_date = validated_data.get('start_date', None),
            end_date = validated_data.get('end_date', None),
            days = validated_data.get('days', None),
            visitor = validated_data.get('visitor', None),
            qr_uuid = str(uuid.uuid4()),
            resident = user.resident,
        )
        return entry_schedule