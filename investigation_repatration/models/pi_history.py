from django.db import models
from base_module.model_mixins import BaseUuidModel
from identifier.identifier import UniqueNonCitizenIdentifierFieldMixin
from ..models import DetentionWarrant, MovementLog, Interaction, PenaltyDecision

class PIHistory(BaseUuidModel, UniqueNonCitizenIdentifierFieldMixin):
    

    '''
    Model records the historical data of PIs' detentions
    '''
    
    detention_warrant = models.ForeignKey(DetentionWarrant, on_delete=models.CASCADE)
    
    movement_log = models.ForeignKey(MovementLog, on_delete=models.CASCADE)
    
    interaction = models.ForeignKey(Interaction, on_delete=models.CASCADE)

    penalty = models.ForeignKey(PenaltyDecision, on_delete=models.CASCADE)
