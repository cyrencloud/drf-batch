from django.urls import path

from .views import Batch

app_name = 'drf_batch'

urlpatterns = [
    path('batch/', Batch.as_view(), name="batch"),
]
