from django.forms import ValidationError
from rest_framework import viewsets

from ..api.serializers import SystemParameterSerializer
from ..models import SystemParameter
from django_filters import rest_framework as filters
from ..filters import SystemParameterFilter
from rest_framework import status
from rest_framework.response import Response


class SystemParameterViewSet(viewsets.ModelViewSet):
    queryset = SystemParameter.objects.all()
    serializer_class = SystemParameterSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SystemParameterFilter

    def create(self, request, *args, **kwargs):
        document_number = request.data.get("document_number")
        if SystemParameter.objects.filter(document_number=document_number).exists():
            return Response(
                {"detail": "SystemParameter with this document number already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )
            # raise ValidationError(
            #     {"detail": "SystemParameter with this document number already exists."}
            # )

        return super().create(request, *args, **kwargs)
