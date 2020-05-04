from django.urls import path


from . import views

app_name = 'createVideo'
urlpatterns = [
    path('crop/<int:id>/', views.crop_image, name='crop_image'),
    path('', views.upload_image, name='create_video'),
]