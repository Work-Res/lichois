from django.db import models


class LocalLanguageKnowledge(models.Model):

    language_name = models.CharField(max_length=100)
    proficiency_level = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.language_name
