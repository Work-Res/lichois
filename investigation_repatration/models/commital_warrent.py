from django.db import models

from base_module.model_mixins import BaseUuidModel
from identifier.non_citizen_identifier_model_mixins import (
    UniqueNonCitizenIdentifierFieldMixin,
)


class CommittalWarrent(UniqueNonCitizenIdentifierFieldMixin, BaseUuidModel):

    committal_warrent = models.FileField(
        verbose_name="Committal Warrent", upload_to="uploads/%Y/%m/%d/"
    )
    # Incarceration Details
    incarceration_date = models.DateField()

    crime_committed = models.TextField()

    sentence_years = models.PositiveIntegerField()
