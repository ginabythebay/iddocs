# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-12 00:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('docs', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='birthcertificate',
            name='location',
        ),
        migrations.DeleteModel(
            name='BirthCertificate',
        ),
    ]
