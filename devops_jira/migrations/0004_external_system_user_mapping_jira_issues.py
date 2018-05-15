# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-05-13 09:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devops_jira', '0003_auto_20180511_1715'),
    ]

    operations = [
        migrations.CreateModel(
            name='External_system_user_mapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_system_username', models.CharField(max_length=255, verbose_name='外部系统用户名')),
                ('external_system_password', models.CharField(max_length=255, verbose_name='外部系统密码')),
                ('external_system', models.CharField(max_length=255, verbose_name='外部系统名称')),
                ('inner_user_group', models.CharField(max_length=10, verbose_name='内部系统账户组')),
                ('inner_user_name', models.CharField(max_length=30, verbose_name='内部系统用户名称')),
            ],
        ),
        migrations.CreateModel(
            name='JIRA_ISSUES',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=100, verbose_name='项目')),
                ('issue_type', models.CharField(max_length=100, verbose_name='问题类型')),
                ('issue_summary', models.CharField(max_length=200, verbose_name='主题')),
                ('issue_priority', models.CharField(max_length=20, verbose_name='优先级')),
                ('issue_reporter', models.CharField(max_length=30, verbose_name='报告人')),
                ('issue_status', models.CharField(max_length=20, verbose_name='状态')),
                ('issue_create_date', models.CharField(max_length=15, verbose_name='创建时间')),
                ('inner_user_group', models.CharField(max_length=10, verbose_name='内部系统账户组')),
                ('inner_user_name', models.CharField(max_length=30, verbose_name='内部系统用户名称')),
            ],
        ),
    ]