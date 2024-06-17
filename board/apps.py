from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
	name = 'board'
	verbose_name = 'Board'
	
	def ready(self):
		import board.signals

