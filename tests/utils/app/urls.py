from django.urls import path, include

from .views import view_200, view_201, view_400


urlpatterns = [
    path('view200/', view_200, name='view-200'),
    path('view201/', view_201, name='view-201'),
    path('view400/', view_400, name='view-400'),
    path('', include('drf_batch.urls', namespace='batch')),
]
