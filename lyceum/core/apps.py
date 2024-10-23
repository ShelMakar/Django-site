import django.apps


class CoreConfig(django.apps.AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = 'Core'


__all__ = ['CoreConfig']
