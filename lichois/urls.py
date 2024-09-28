"""
URL configuration for lichois project.

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

from django.conf import settings
from django.conf.urls.static import static

from drf_yasg import openapi
from rest_framework import permissions
from drf_yasg.views import get_schema_view

from django.contrib import admin
from django.urls import path, include

from app.admin_site import app_admin
from board.admin_site import board_admin

schema_view = get_schema_view(
    openapi.Info(
        title="Africort Technologies",
        default_version="v1",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("board/", board_admin.urls),
    path("app/", app_admin.urls),
    path("lichois/api/v1/", include("app.urls")),
    path("lichois/api/v1/", include("app_address.urls")),
    path("lichois/api/v1/", include("app_checklist.urls")),
    path("lichois/api/v1/", include("app_comments.urls")),
    path("lichois/api/v1/", include("app_contact.urls")),
    path("lichois/api/v1/", include("app_attachments.urls")),
    # path('lichois/api/v1/', include('app_search.urls')),
    path("lichois/api/v1/", include("app_personal_details.urls")),
    path("lichois/api/v1/", include("workresidentpermit.urls")),
    path("lichois/api/v1/", include("board.urls")),
    path("lichois/api/v1/", include("visa.urls")),
    path("lichois/api/v1/", include("workflow.urls")),
    path("lichois/api/v1/", include("app_assessment.urls")),
    path("lichois/api/v1/", include("app_production.urls")),
    path("lichois/api/v1/", include("crm_integration.urls")),
    path("lichois/api/v1/", include("permanent_residence.urls")),
    path(
        "lichois/docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "lichois/redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    path("lichois/api/v1/", include("authentication.urls")),
    path("lichois/api/v1/", include("app_checklist.urls")),
    path("lichois/api/v1/", include("travel.urls")),
    path("lichois/api/v1/", include("app_notification.urls")),
    path("lichois/api/v1/", include("blue_card.urls")),
    path("lichois/api/v1/", include("citizenship.urls")),
    path("lichois/api/v1/", include("gazette.urls")),
    path("lichois/api/v1/", include("non_citizen_profile.urls")),
    path("lichois/api/v1/", include("investigation_repatration.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
