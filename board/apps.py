from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
	name = 'board'
	icon = 'fa fa-folder-open-o'
	verbose_name = 'Board'
	
	def ready(self):
		import board.signals

