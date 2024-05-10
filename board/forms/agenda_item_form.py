from django import forms
from ..models import AgendaItem


class AgendaItemForm(forms.ModelForm):
	class Meta:
		model = AgendaItem
		fields = '__all__'
