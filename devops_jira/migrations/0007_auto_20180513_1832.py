# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-05-13 10:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devops_jira', '0006_auto_20180513_1827'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jira_issues',
            old_name='issue_type',
            new_name='issue_type_name',
        ),
        migrations.AddField(
            model_name='jira_issues',
            name='issue_type_id',
            field=models.CharField(max_length=20, null=True, verbose_name='问题类型ID'),
        ),
        migrations.AddField(
            model_name='jira_issues',
            name='project_Id',
            field=models.CharField(max_length=20, null=True, verbose_name='项目Id'),
        ),
    ]
