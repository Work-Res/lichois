from django.db import models


class Permission(models.Model):
	name = models.CharField(max_length=190)
	pass
