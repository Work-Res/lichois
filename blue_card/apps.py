<<<<<<< HEAD
from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "blue_card"
=======
from django.apps import AppConfig


class BlueCardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blue_card'
>>>>>>> aa5e5a9 (feat(BlueCard): :sparkles: Added new service (blue card))
