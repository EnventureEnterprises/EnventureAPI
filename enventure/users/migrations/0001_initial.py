# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-07-27 18:29
from __future__ import unicode_literals

import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=30, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.')], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('avatar', models.CharField(default='http://urb.sparkpl.ug/static/images/avatar.png', max_length=200)),
                ('karma', models.IntegerField(default=1)),
                ('mobile', models.CharField(blank=True, max_length=200, null=True)),
                ('gender', models.CharField(blank=True, max_length=6, null=True)),
                ('post_views', models.IntegerField(blank=True, default=0, null=True)),
                ('post_shares', models.IntegerField(blank=True, default=0, null=True)),
                ('notify_of_friend_activity', models.NullBooleanField()),
                ('notify_of_comments', models.NullBooleanField()),
                ('notify_of_likes', models.NullBooleanField()),
                ('is_facebook', models.NullBooleanField()),
                ('is_twitter', models.NullBooleanField()),
                ('current_login', models.CharField(blank=True, max_length=200, null=True)),
                ('is_mobile', models.NullBooleanField()),
                ('posts_count', models.IntegerField(blank=True, default=0, null=True)),
                ('likes_count', models.IntegerField(blank=True, default=0, null=True)),
                ('unread_notifications_count', models.IntegerField(blank=True, default=0, null=True)),
                ('send_newsletter', models.NullBooleanField()),
                ('is_registered', models.NullBooleanField()),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
