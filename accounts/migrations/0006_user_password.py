# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-21 16:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20170321_0150'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default='a', max_length=50),
            preserve_default=False,
        ),
    ]
