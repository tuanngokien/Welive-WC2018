from django.apps import AppConfig


class WebhookConfig(AppConfig):
    name = 'webhook'

    def ready(self):
        import webhook.handlers
