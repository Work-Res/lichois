from rest_framework import viewsets

from .filter import CommentFilter
from ..models import Comment
from ..api.serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = "document_number"
    filterset_class = CommentFilter
