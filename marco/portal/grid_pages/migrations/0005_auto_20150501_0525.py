# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grid_pages', '0004_gridpagedetail_url_override'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gridpagedetail',
            name='url_override',
            field=models.CharField(help_text=b'Overrides Default Slug on Welcome Page (ex. /[actual_slug]/)', max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
