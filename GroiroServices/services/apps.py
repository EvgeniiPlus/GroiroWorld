from django.apps import AppConfig

class usersConfig(AppConfig):
    name = 'users'

    def ready(self):
        import GroiroServices.services.signals

class ServicesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'services'
