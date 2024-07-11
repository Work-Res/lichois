from django.db import models


from app.models import ApplicationBaseModel


class Declaration(ApplicationBaseModel):

    declaration_fname = models.CharField(
        verbose_name="Declaration firstname", max_length=150
    )

    declaration_lname = models.CharField(
        verbose_name="Declaration lastname", max_length=150
    )

    declaration_date = models.DateField(
        # validation=date_not_future
    )

    signature = models.CharField(max_length=190)

    class Meta:
        verbose_name = "Declaration"
