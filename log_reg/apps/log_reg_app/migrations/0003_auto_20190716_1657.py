# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-07-16 16:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('log_reg_app', '0002_auto_20190716_0029'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comment',
            new_name='content',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='message',
            new_name='content',
        ),
    ]