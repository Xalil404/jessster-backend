from django.apps import AppConfig


class BlogapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blogAPI'

    def ready(self):
        import blogAPI.signals
