from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
	phone_number = models.IntegerField(unique=True, null=True)
	
	def is_chairperson(self):
		return self.groups.filter(name='chair_person').exists()
	
	def is_board_member(self):
		return self.groups.filter(name='board_member').exists()
	
	def is_secretary(self):
		return self.groups.filter(name='secretary').exists()
