# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-10 15:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, upload_to=b'profile_image'),
        ),
    ]
