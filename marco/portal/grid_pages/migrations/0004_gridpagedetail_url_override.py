# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grid_pages', '0003_auto_20150429_1844'),
    ]

    operations = [
        migrations.AddField(
            model_name='gridpagedetail',
            name='url_override',
            field=models.CharField(help_text=b'Overrides Default Slug on Welcome Page', max_length=255, null=True),
            preserve_default=True,
        ),
    ]
