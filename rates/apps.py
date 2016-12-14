from exchange_rates import app

from django.apps import apps, AppConfig


class RatesConfig(AppConfig):
    name = 'rates'

    def ready(self):
        # Using a string here means the worker will not have to
        # pickle the object when using Windows.
        app.config_from_object('django.conf:settings')
        installed_apps = [
            app_config.name for app_config in apps.get_app_configs()
        ]
        app.autodiscover_tasks(lambda: installed_apps, force=True)

        app.conf.beat_schedule = {
            'fetch-rates': {
                'task': 'rates.tasks.fetch_rates',
                'schedule': 15.0,
            },
        }
