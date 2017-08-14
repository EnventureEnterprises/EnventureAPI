# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-08-11 11:36
from __future__ import unicode_literals

from django.db import migrations
import location_field.models.spatial
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('bookkeeping', '0003_auto_20170811_0940'),
    ]

    operations = [
       
        migrations.AlterField(
            model_name='item',
            name='image',
            field=versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to='files/%Y/%m/%d'),
        ),
    ]
