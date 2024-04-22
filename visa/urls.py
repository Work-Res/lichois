from django.urls import path, include
from django.urls.conf import path
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from .views import BlueCardApplicationViewSet, BlueCardViewSet
from .views import ContactMethodViewSet, DisposalMoneySerializer
from .views import ExemptionCertificateApplicationViewSet, ExemptionCertificateViewSet
from .views import ExemptionCertificateDependantViewSet, VisaApplicationViewSet
from .views import VisaReferenceViewSet, VisaViewSet
from .admin_site import visa_admin

app_name = 'visa'

router = DefaultRouter()
router.register(r'blue-cards-applications/', BlueCardApplicationViewSet, basename='blue-cards-applications')
router.register(r'blue-cards', BlueCardViewSet, basename='blue-cards')
router.register(r'exemption-cert-applications', ExemptionCertificateApplicationViewSet,
                basename='exemption-cert-applications')
router.register(r'exemption-certificates', ExemptionCertificateViewSet, basename='exemption-certificates')
router.register(r'visa-applications', VisaApplicationViewSet, basename='visa-applications')
router.register(r'visas', VisaViewSet, basename='visas')


urlpatterns = [
    path('admin/', visa_admin.urls),
    path('', RedirectView.as_view(url='admin/'), name='home_url'),
    path('', include(router.urls)),

]

