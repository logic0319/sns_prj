# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-09 20:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_alarm'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alarm',
            name='comment_author',
        ),
        migrations.RemoveField(
            model_name='alarm',
            name='post',
        ),
        migrations.AddField(
            model_name='post',
            name='is_bookmarked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='is_like',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='modified_date',
            field=models.DateTimeField(),
        ),
        migrations.DeleteModel(
            name='Alarm',
        ),
    ]
