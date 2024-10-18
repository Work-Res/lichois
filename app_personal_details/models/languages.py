from django.db import models
from app.models import ApplicationBaseModel




class Languages(ApplicationBaseModel):

    no = models.CharField(max_length=150)

    languages = models.CharField(max_length=150)


    class Meta:
        verbose_name = "Language"
        verbose_name_plural = "Languages"