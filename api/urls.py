from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token
from .view import resident,announcement,securityGuard,visitor,notification,bill
router = routers.DefaultRouter()
router.register(r'resident',resident.ResidentViewSet,basename="resident")
router.register(r'resident_request',resident.RequestViewSet,basename="resident_request")
router.register(r'property',resident.PropertyViewSet,basename="property_list")
router.register(r'announcements',announcement.AnnouncementViewSet,basename="announcement")
router.register(r'get_primary',securityGuard.GetPrimaryViewSet,basename="security_primary")
router.register(r'reasons',securityGuard.ReasonViewSet)
router.register(r'security_passnumber',securityGuard.PassNumberViewSet)
router.register(r'security_devicenumber',securityGuard.DeviceNumberViewSet)
router.register(r'security_street',securityGuard.SecStreetViewSet)
router.register(r'security_postlog',securityGuard.PostLogViewSet,basename="security_postlog")
router.register(r'security_resident',securityGuard.SecResidentViewSet,basename="security_resident")
router.register(r'security_ipcam',securityGuard.SecIPCamViewSet)
router.register(r'security_boomgate',securityGuard.BoomgateViewSet)
router.register(r'security_boomgatelog',securityGuard.SecBoomgateLogViewSet,basename='boomgatelog')
router.register(r'visitor_entry',visitor.TrackEntryViewSet,basename='visitor_entry')
router.register(r'visitors',visitor.VisitorViewSet,basename='visitor')
router.register(r'entry_schedule',visitor.EntryScheduleViewSet,basename='entry_schedule')
router.register(r'notification',notification.NotificationViewSet,basename='notification')
router.register(r'forgot',resident.PasswordRecoveryViewSet,basename='forgot')
router.register(r'change_password',resident.ChangePasswordViewSet,basename='change_password')
router.register(r'request_family',resident.RequestFamilyViewSet,basename='request_family')
router.register(r'billing',bill.BillingViewSet,basename='billing')
urlpatterns = [
    path('',include(router.urls)),
    path('login/', resident.custom_obtain_jwt_token), 
    path('verify_token/', verify_jwt_token),
    path('security_login/',securityGuard.SecurityLogin.as_view()),
    path('security_verify_token/',securityGuard.SVerifyJSONWebToken.as_view())
    
]

