from django.db import models
from django.contrib.postgres.fields import ArrayField

class VideoTemplate(models.Model):
    name = models.CharField(max_length=100)
    background_clip = models.FileField()
    faces_count = models.IntegerField()

class FaceInsert(models.Model):
    template = models.ForeignKey(VideoTemplate, on_delete=models.PROTECT)
    creation_datetime = models.DateTimeField(auto_now_add=True)
