# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-04 01:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meitu', '0003_img_origin'),
    ]

    operations = [
        migrations.AddField(
            model_name='img',
            name='saved_num',
            field=models.IntegerField(default=0),
        ),
    ]
