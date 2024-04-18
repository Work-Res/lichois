from haystack import indexes

from app.models import ApplicationVersion


class ApplicationVersionIndex(indexes.ModelSearchIndex, indexes.Indexable):

    class Meta:
        model = ApplicationVersion
