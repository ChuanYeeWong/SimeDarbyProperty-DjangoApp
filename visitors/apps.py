from django.apps import AppConfig


class VisitorsConfig(AppConfig):
    name = 'visitors'
    def ready(self):
        import visitors.signals  # noqa