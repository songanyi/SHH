# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-07 16:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('habitat', '0013_images_prop'),
    ]

    operations = [
        migrations.RenameField(
            model_name='images',
            old_name='prop',
            new_name='pid',
        ),
    ]
