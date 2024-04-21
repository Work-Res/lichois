from django.db import models
from base_module.model_mixins import BaseUuidModel


class EmergencyResidencePermit(BaseUuidModel):

	class Meta:
		app_label = 'work_residence_permit'
