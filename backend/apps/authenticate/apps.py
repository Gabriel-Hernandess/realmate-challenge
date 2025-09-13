from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.utils import OperationalError

class AuthenticateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.authenticate'