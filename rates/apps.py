from exchange_rates import app

from django.apps import apps, AppConfig


class RatesConfig(AppConfig):
    name = 'rates'

    def ready(self):
        app.config_from_object('django.conf:settings')
        installed_apps = [
            app_config.name for app_config in apps.get_app_configs()
        ]
        app.autodiscover_tasks(lambda: installed_apps, force=True)
