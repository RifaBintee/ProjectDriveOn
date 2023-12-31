from django.apps import AppConfig


class CusprofileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cusProfile'

    def ready(self):
        import cusProfile.signals
