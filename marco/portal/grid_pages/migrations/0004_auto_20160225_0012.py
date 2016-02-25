# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grid_pages', '0003_auto_20150429_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gridpagesection',
            name='media_embed_url',
            field=models.URLField(help_text=b"The URL to a video that you'd like to embed, e.g., https://vimeo.com/121095661.", blank=True),
            preserve_default=True,
        ),
    ]
