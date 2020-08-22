from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/error_graph/', consumers.ErrorGraphConsumer),
]