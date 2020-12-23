from django.urls import path
from .views import calculate

app_name = 'mesurements'


urlpatterns = [
    path('', calculate,name='calculate')
]
