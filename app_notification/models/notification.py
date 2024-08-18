from base_module.model_mixins import BaseUuidModel
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from authentication.models import User
from django.contrib.postgres.fields import JSONField


class Notification(BaseUuidModel, models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
	object_id = models.PositiveIntegerField(null=True, blank=True)
	content_object = GenericForeignKey('content_type', 'object_id')
	message = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	is_read = models.BooleanField(default=False)
	has_attachment = models.BooleanField(default=False)
	retry_count = models.IntegerField(null=True, blank=True)
	context = JSONField(null=True, blank=True)
	template_name = models.CharField(max_length=255, null=True, blank=True)

	def __str__(self):
		return f'Notification for {self.user.name}'
