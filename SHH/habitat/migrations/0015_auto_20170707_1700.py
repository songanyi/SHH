# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-07 17:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('habitat', '0014_auto_20170707_1653'),
    ]

    operations = [
        migrations.RenameField(
            model_name='images',
            old_name='pid',
            new_name='prop_id',
        ),
    ]
