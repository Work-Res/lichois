from django.contrib import admin
from ..admin_site import decision_admin
from ..models import BoardDecision
from ..forms import ApplicationRecommendationForm


@admin.register(BoardDecision, site=decision_admin)
class ApplicationApplicationRecommendationAdmin(admin.ModelAdmin):

    form = ApplicationRecommendationForm
