from django.urls import path

from . import views

app_name = 'kaupapaapp'
urlpatterns = [
    path('', views.create_video, name='create_video'),
]