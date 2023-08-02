from django.apps import AppConfig


class EquConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'equ'

    def ready(self):
        from equ import signals
