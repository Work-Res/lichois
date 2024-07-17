from django.db import models
from django.contrib.contenttypes.models import ContentType


class ParentModelManager(models.Manager):

    def __init__(self, app_label=None, model_name=None):
        super().__init__()
        self.app_label = app_label
        self.model_name = model_name
        self.model = self.get_model()

    def get_model(self):
        content_type = ContentType.objects.get(app_label=self.app_label, model=self.model_name)
        return content_type.model_class()
