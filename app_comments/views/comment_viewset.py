from rest_framework import viewsets
from ..models import Comment
from ..api.serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer
