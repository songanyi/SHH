# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-04 07:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habitat', '0005_auto_20170704_0704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='property_type',
            field=models.CharField(choices=[('old_house', 'Old house'), ('high_rise', 'High-rise'), ('villa', 'Villa'), ('service_apt', 'Service Apartment')], default='0', max_length=50),
        ),
        migrations.AlterField(
            model_name='property',
            name='room_type',
            field=models.CharField(choices=[('studio', 'Studio'), ('one_br', '1BR'), ('two_br', '2BR'), ('three_br', '3BR')], default='0', max_length=50),
        ),
    ]
