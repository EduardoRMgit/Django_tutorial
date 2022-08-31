from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class PldConfig(AppConfig):
    name = 'pld'

    def ready(self):
        autodiscover_modules('signals')
        autodiscover_modules('receivers')
