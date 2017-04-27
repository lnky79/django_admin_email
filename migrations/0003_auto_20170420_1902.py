# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-20 11:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mail', '0002_auto_20170420_0031'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mail',
            options={'verbose_name': '用户意见', 'verbose_name_plural': '* 用户意见箱'},
        ),
        migrations.AddField(
            model_name='mailrecord',
            name='err_msg',
            field=models.TextField(null=True, verbose_name='异常消息'),
        ),
        migrations.AddField(
            model_name='mailrecord',
            name='success',
            field=models.BooleanField(default=True, verbose_name='发送成功'),
        ),
    ]