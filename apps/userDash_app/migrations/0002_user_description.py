# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-28 18:57
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('userDash_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='description',
            field=models.TextField(default=datetime.datetime(2016, 6, 28, 18, 57, 6, 993658, tzinfo=utc), max_length=200),
            preserve_default=False,
        ),
    ]
