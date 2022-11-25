from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class CoreConfig(AppConfig):
    name = 'core'
    verbose_name = 'Core'

    def ready(self):
        autodiscover_modules('receivers')
