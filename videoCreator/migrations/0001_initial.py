# Generated by Django 3.0.5 on 2020-05-01 13:04

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VideoTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('background_clip', models.FileField(upload_to='')),
                ('faces_count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='FaceInsert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('faces', django.contrib.postgres.fields.ArrayField(base_field=models.FileField(upload_to=''), size=None)),
                ('creation_datetime', models.DateTimeField(auto_now_add=True)),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='videoCreator.VideoTemplate')),
            ],
        ),
    ]
