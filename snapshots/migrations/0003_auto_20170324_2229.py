# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-24 22:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snapshots', '0002_publication'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='publication',
            options={'permissions': (('can_publish', 'Can create snapshots, publish them'),)},
        ),
    ]
