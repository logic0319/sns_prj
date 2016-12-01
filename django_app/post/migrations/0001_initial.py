# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-01 09:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HashTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('modified_date', models.DateTimeField(auto_now_add=True)),
                ('view_count', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('bookmark_users', models.ManyToManyField(related_name='bookmark_users_set', to=settings.AUTH_USER_MODEL)),
                ('hashtags', models.ManyToManyField(to='post.HashTag')),
                ('like_users', models.ManyToManyField(related_name='like_users_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]