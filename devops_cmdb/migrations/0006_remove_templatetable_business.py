# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-19 07:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devops_cmdb', '0005_auto_20181112_1543'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='templatetable',
            name='business',
        ),
    ]