from django.db import models


class FamilyMember(models.Model):
    RELATIONSHIP_CHOICES = [
        ('brother', 'Brother'),
        ('sister', 'Sister'),
        ('uncle', 'Uncle'),
        ('aunt', 'Aunt'),
    ]

    name = models.CharField(max_length=255)  # Full name of the family member
    address = models.CharField(max_length=255)  # Address of the family member
    relationship = models.CharField(max_length=10, choices=RELATIONSHIP_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.relationship})"
