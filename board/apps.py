from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
	name = 'board'
	icon = 'fa fa-folder-open-o'
	verbose_name = 'Board'
	
	def ready(self):
		from board.models import board_meeting_on_post_save
		from board.signals import create_application_decision, create_board_decision

