from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
	name = 'board'
	icon = 'fa fa-folder-open-o'
	verbose_name = 'Board'
	
	def ready(self):
		from .models import board_meeting_on_post_save
		from .signals import create_application_decision
		from .signals import create_board_decision
