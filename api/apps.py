from django.apps import AppConfig

from api.firebase.init_firebase import initFireBase


class ApiConfig(AppConfig):
    name = 'api'

    def create(cls, entry):
        return super().create(entry)

    def ready(self):
        super().ready()
        print("django api config ready")
        initFireBase()
