from django.urls import path
from rest_api.views import hello_world

app_name = 'rest_api'
urlpatterns = [
    path('hello_world', hello_world, name='hello_world_api')
]

