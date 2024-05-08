from django.contrib import admin
from ..admin_site import board_admin
from ..models import BoardDecision
from ..forms import ApplicationRecommendationForm


@admin.register(BoardDecision, site=board_admin)
class ApplicationApplicationRecommendationAdmin(admin.ModelAdmin):

    form = ApplicationRecommendationForm
