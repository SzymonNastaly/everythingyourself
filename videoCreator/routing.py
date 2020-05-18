from django.urls import re_path

from . import consumers

# videoprogress supposed to ping client regularly to 1. reset request time limit and 2. give info about progress
websocket_urlpatterns = [
    re_path(r'ws/videoprogress/(?P<id>[0-9]+)/$', consumers.VideoConsumer),
]