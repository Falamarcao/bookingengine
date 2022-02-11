from .views import Units
from django.urls import path

app_name = 'api'

urlpatterns = [
        path('v1/units/', Units.as_view(), name='units'),
]