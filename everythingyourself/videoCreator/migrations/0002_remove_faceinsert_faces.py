# Generated by Django 3.0.5 on 2020-05-05 19:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videoCreator', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='faceinsert',
            name='faces',
        ),
    ]