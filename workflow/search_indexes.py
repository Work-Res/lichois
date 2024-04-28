from haystack import indexes
from .models import Task


class TasksIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    created = indexes.DateTimeField(model_attr='created')
    status = indexes.CharField()
    assignee_name = indexes.CharField()
    activity_name = indexes.CharField()

    def prepare_assignee_name(self, obj):
        return obj.assignee.username if obj.assignee else ''

    def prepare_activity_name(self, obj):
        return obj.activity.name if obj.activity else ''

    def get_model(self):
        return Task

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
