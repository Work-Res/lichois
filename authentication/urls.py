"""
URL configuration for authentication project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import (LogoutView, UserView, OtpEmailVerificationView, PasswordResetView,
                    ChangePasswordView)
from .admin_site import authentication_admin

urlpatterns = [
    
    path("authentication/", authentication_admin.urls),
	path('admin/', admin.site.urls),
    
	path('logout/', LogoutView.as_view(), name='logout'),
	path('user/', UserView.as_view(), name='user'),
	path('otp-email-verification/', OtpEmailVerificationView.as_view(), name='otp_email_verification'),
	path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
	path('change-password/', ChangePasswordView.as_view(), name='change_password'),
	path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
	path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
	path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
