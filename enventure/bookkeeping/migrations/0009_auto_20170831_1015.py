# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-08-31 10:15
from __future__ import unicode_literals

from django.db import migrations, models
import location_field.models.spatial


class Migration(migrations.Migration):

    dependencies = [
        ('bookkeeping', '0007_auto_20170831_1007'),
    ]

    operations = [
        migrations.AddField(
            model_name='cbo',
            name='email',
            field=models.EmailField(blank=True, max_length=200, null=True),
        ),
    ]
