from django.urls import path


from . import views

app_name = 'createVideo'
urlpatterns = [
    path('create/<int:id>', views.video_create, name='video_create'),
    path('crop/<int:id>/', views.image_crop, name='image_crop'),
    path('', views.image_upload, name='image_upload'),
]