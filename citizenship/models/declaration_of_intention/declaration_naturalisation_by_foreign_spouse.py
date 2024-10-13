from django.db import models
from app.models import ApplicationBaseModel
from citizenship.models.residential_history import ResidentialHistory

from base_module.model_mixins import DeclarationModelMixin, CommissionerOathModelMixin


class DeclarationNaturalisationByForeignSpouse(ApplicationBaseModel, DeclarationModelMixin, CommissionerOathModelMixin):

    application_residential_history = models.OneToOneField(
        ResidentialHistory, on_delete=models.CASCADE,  null=True, blank=True)

    class Meta:
        verbose_name = ('Declaration On Intention To Make An Application For A Certificate'
                        ' Of Naturalisation By A Foreign Spouse(FormK)')
        app_label = 'citizenship'
        db_table = 'citizenship_decl_intention'

    def __str__(self):
        return f"Declaration of Intention by Foreign Spouse - {self.id}"
