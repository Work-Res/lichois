import django_filters

from app_comments.models import Comment


class CommentFilter(django_filters.FilterSet):
    document_number = django_filters.CharFilter(lookup_expr='iexact')
    user = django_filters.CharFilter(field_name='user__username', lookup_expr='icontains')
    comment_type = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Comment
        fields = ['document_number', 'user', 'comment_type']
