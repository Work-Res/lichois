from rest_framework import viewsets
from ..models import AuthorizeDetention
from api.serializers import AuthorizeDetentionSerializer


class AuthorizeDetentionViewSet(viewsets.ModelViewSet):
    queryset = AuthorizeDetention.objects.all()
    serializer_class = AuthorizeDetentionSerializer
