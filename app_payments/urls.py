from rest_framework.routers import DefaultRouter
from app_payments.api import PaymentViewSet

from django.urls import path, include

from app_payments.views import PaymentRequestView, CyberSourceResponseView

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('api/', include(router.urls)),
    path('payment/request/', PaymentRequestView.as_view(), name='payment-request'),
    path('payment/response/', CyberSourceResponseView.as_view(), name='payment-response'),
]
