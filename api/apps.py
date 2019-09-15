from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'api'

    def create(cls, entry):
        return super().create(entry)

    def ready(self):
        super().ready()
        print("django api config ready")
        return "Hello Django"
