# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-12 00:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import markdownx.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BirthCertificate',
            fields=[
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('article', markdownx.models.MarkdownxField(help_text='Markdown please')),
                ('location', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='locations.Location')),
            ],
        ),
    ]
