from django.apps import AppConfig

class FinalappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'FinalApp'

    def ready(self):
        import FinalApp.models  # This loads the signal
