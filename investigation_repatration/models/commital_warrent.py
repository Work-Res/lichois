from django.db import models

from base_module.model_mixins import BaseUuidModel
from identifier import UniqueNonCitizenIdentifierFieldMixin


class CommittalWarrent(UniqueNonCitizenIdentifierFieldMixin, BaseUuidModel):

    committal_warrent = models.FileField(
        verbose_name="Committal Warrent", upload_to="uploads/%Y/%m/%d/"
    )
