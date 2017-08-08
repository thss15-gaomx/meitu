# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-05 09:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meitu', '0009_img_is_con'),
    ]

    operations = [
        migrations.CreateModel(
            name='Remark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=250)),
                ('remark_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AddField(
            model_name='img',
            name='is_emb',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='remark',
            name='pic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='meitu.IMG'),
        ),
        migrations.AddField(
            model_name='remark',
            name='remarker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
