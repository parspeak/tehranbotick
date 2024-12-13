from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MediasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'medias'
    verbose_name = _("Media Management")
