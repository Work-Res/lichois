from django.db import models


class Role(models.Model):
	name = models.CharField(max_length=190)
	description = models.TextField()
	active = models.BooleanField(default=True)
