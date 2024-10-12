from django.db import models


class NationalityDetails(models.Model):

    birth_citizenship = models.CharField(max_length=190)
    present_citizenship = models.CharField(max_length=190)
    other_prev_citizenship = models.TextField(max_length=300)

    class Meta:
        abstact = True
