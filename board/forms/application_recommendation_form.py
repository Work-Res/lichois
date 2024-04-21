from django import forms
from ..models import BoardDecision


class ApplicationRecommendationForm(forms.ModelForm):

    class Meta:
        model = BoardDecision
        fields = '__all__'
