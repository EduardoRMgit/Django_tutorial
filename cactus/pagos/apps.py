from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class PagosConfig(AppConfig):
    name = 'pagos'

    def ready(self):
        autodiscover_modules('signals')
        autodiscover_modules('receivers')
