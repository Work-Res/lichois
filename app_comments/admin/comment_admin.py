from django.contrib import admin
from ..admin_site import comment_admin
from ..models import Comment
from ..forms import CommentForm


@admin.register(Comment, site=comment_admin)
class CommentAdmin(admin.ModelAdmin):

    form = CommentForm
