from django.urls import path

from .views import (
    CreateNonCitizenProfileView,
    GetNonCitizenProfileView,
    NonCitizenProfilesView,
)

urlpatterns = [
    path(
        "get-profile/<str:non_citizen_identifier>/",
        GetNonCitizenProfileView.as_view(),
        name="get-non-citizen-profile-view",
    ),
    path(
        "create-profile/",
        CreateNonCitizenProfileView.as_view(),
        name="create-non-citizen-profile-view",
    ),
    path(
        "profiles/",
        NonCitizenProfilesView.as_view(),
        name="non-citizen-profiles-view",
    ),
]
