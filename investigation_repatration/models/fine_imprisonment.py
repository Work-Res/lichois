from django.db import models
from base_module.model_mixins import BaseUuidModel
from identifier.identifier import UniqueNonCitizenIdentifierFieldMixin

choices=[
            ('Low', 'Low'),
            ('Medium', 'Medium'),
            ('High', 'High')
        ] 

class PenaltyDecision(BaseUuidModel, UniqueNonCitizenIdentifierFieldMixin):

    '''
    Model records decisions related to penalties awarded to PIs.
    '''    
    
    reason_for_violation = models.CharField(max_length=255)  
    
    severity_level = models.CharField(max_length=50,choices=choices)
    
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    imprisonment_duration = models.DurationField(null=True, blank=True)
    
    decision_date = models.DateTimeField(auto_now_add=True)
    
    decided_by = models.CharField(max_length=255)
    
    additional_notes = models.TextField(null=True, blank=True)  

    def __str__(self):
        return f"Decision for {self.pi.name} - Severity: {self.severity_level} - Date: {self.decision_date}"


    def apply_penalty(self):
        """
        Applies the penalty based on the decision made.

        TODO: Add actual penalties
        """
        if self.severity_level == 'Low':
            self.fine_amount = 100
            self.imprisonment_duration = None
        elif self.severity_level == 'Medium':
            self.fine_amount = 500
            self.imprisonment_duration = None
        elif self.severity_level == 'High':
            self.fine_amount = 1000
            self.imprisonment_duration = '30 days'
        
        self.save()
