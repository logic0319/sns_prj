# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-11 22:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0009_auto_20161211_2007'),
    ]

    operations = [
        migrations.AddField(
            model_name='alarm',
            name='content',
            field=models.TextField(blank=True),
        ),
    ]