from rest_framework import serializers
from ...models import Examiner


class ExaminerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Examiner
        fields = "__all__"
