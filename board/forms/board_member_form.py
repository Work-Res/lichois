from django import forms
from ..models import BoardMember


class BoardMemberForm(forms.ModelForm):

    class Meta:
        model = BoardMember
        fields = '__all__'
