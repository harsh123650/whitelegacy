# dairyapp/apps.py
from django.apps import AppConfig

class DairyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dairyapp'

    def ready(self):
        import dairyapp.signals
