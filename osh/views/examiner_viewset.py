from rest_framework import viewsets
from ..models import Examiner
from ..api.serializers import ExaminerSerializer


class ExaminerViewSet(viewsets.ModelViewSet):
    queryset = Examiner.objects.all()
    serializer_class = ExaminerSerializer
    