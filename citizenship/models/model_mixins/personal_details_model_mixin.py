from django.db import models


class PersonalDetailsModelMixin(models.Model):

    last_name = models.CharField(max_length=190)
    first_name = models.CharField(max_length=190)
    middle_name = models.CharField(max_length=190,blank=True,null=True)
    maiden_name = models.CharField(max_length=190,blank=True,null=True)

    class Meta:
        abstract = True
