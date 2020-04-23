from django.urls import re_path

from . import consumers
from . import cli_consumers

websocket_urlpatterns = [
    re_path(r'run-env/(?P<env>\w+)/$', consumers.BackendConsumer),
    re_path(r'connection-cli/$', cli_consumers.CliConsumer),
]