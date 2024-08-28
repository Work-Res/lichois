from django.urls import path
from .views import NonCitizenProfileView


urlpatterns = [
    path(
        "non-citizen-profile/",
        NonCitizenProfileView.as_view(),
        name="non-citizen-profile-view",
    ),
]
