# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-05-11 09:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devops_jira', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='JIRA_FIELDS_CONFIG',
            new_name='FIELDS_CONFIG',
        ),
    ]
