# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-05 19:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20171104_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='response',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='app.Question'),
        ),
    ]