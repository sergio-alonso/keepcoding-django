# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-24 17:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0009_post_published'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='published',
        ),
    ]
