# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grid_pages', '0002_auto_20150429_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gridpagedetail',
            name='metric',
            field=models.CharField(max_length=4, null=True, blank=True),
            preserve_default=True,
        ),
    ]
