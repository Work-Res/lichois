from django.db import models

from app.models import ApplicationBaseModel


class Assessment(ApplicationBaseModel):

    competency = models.IntegerField(default=0)
    qualification = models.IntegerField(default=0)
    employer_justification = models.IntegerField(default=0)
    scarce_skill = models.IntegerField(default=0)
    work_experience = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    marking_score = models.JSONField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.save_assessment()

    class Meta:

        db_table = "assessment"
        verbose_name = "Assessment"
        verbose_name_plural = "Assessments"
        ordering = ["-competency", "qualification"]

    def __str__(self):
        return f"Assessment: {self.competency}, {self.qualification}"
