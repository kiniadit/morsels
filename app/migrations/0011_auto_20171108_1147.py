# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-08 19:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20171108_1104'),
    ]

    operations = [
        migrations.RenameField(
            model_name='anonymoususer',
            old_name='phone_number',
            new_name='phonenumber',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='phone_number',
            new_name='phonenumber',
        ),
    ]
