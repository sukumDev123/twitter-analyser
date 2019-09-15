from django.contrib import admin
from django.urls import path
from api.views import searchHashtagAndWriteFileCsv, handleDataCsv
urlpatterns = [
    path("twitter/searchHashtagAndWriteFileCsv", searchHashtagAndWriteFileCsv),
    path('twitter/handleDataCsv', handleDataCsv)
]
