from django.db import models


class NationalityDetailsModelMixin(models.Model):

    birth_citizenship = models.CharField(max_length=190, null=True, blank=True)
    present_citizenship = models.CharField(max_length=190, null=True, blank=True)
    other_prev_citizenship = models.TextField(max_length=300, null=True, blank=True)

    class Meta:
        abstract = True
