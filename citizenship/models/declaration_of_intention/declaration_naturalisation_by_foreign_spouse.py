from django.db import models
from app.models import ApplicationBaseModel
from app_address.models.application_address import ApplicationAddress
from app_contact.models.application_contact import ApplicationContact
from citizenship.models.residential_history import ResidentialHistory
from citizenship.models.model_mixins.nationality_model_mixin import NationalityDetailsModelMixin
from app_personal_details.models import Person


class DeclarationNaturalisationByForeignSpouse(ApplicationBaseModel,
                                               NationalityDetailsModelMixin,models.Model
                                               ):
    application_person = models.OneToOneField(Person, on_delete=models.CASCADE,  null=True, blank=True)
    application_address = models.OneToOneField(ApplicationAddress, on_delete=models.CASCADE,  null=True, blank=True)
    application_contact = models.OneToOneField(ApplicationContact, on_delete=models.CASCADE,  null=True, blank=True)
    application_residential_history = models.OneToOneField(ResidentialHistory, on_delete=models.CASCADE,  null=True, blank=True)

    class Meta:
        verbose_name = ('Declaration On Intention To Make An Application For A Certificate'
                        ' Of Naturalisation By A Foreign Spouse(FormK)')
        app_label = 'citizenship'
