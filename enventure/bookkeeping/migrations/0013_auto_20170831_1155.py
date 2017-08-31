# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-08-31 11:55
from __future__ import unicode_literals

from django.db import migrations, models
import location_field.models.spatial


class Migration(migrations.Migration):

    dependencies = [
        ('bookkeeping', '0012_auto_20170831_1151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cbo',
            name='cboName',
            field=models.CharField(blank=True, default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cbo',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=200),
            preserve_default=False,
        ),
       
        migrations.AlterField(
            model_name='enventure',
            name='email',
            field=models.EmailField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='enventure',
            name='phoneNumber',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]