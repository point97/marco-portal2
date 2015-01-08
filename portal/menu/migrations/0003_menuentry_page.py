# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0010_change_page_owner_to_null_on_delete'),
        ('menu', '0002_menuentry_show_divider_underneath'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuentry',
            name='page',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailcore.Page', null=True),
            preserve_default=True,
        ),
    ]
