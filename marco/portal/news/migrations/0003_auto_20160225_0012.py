# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_auto_20150522_0047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storysection',
            name='media_embed_url',
            field=models.URLField(help_text=b"The URL to a video that you'd like to embed, e.g., https://vimeo.com/121095661.", blank=True),
            preserve_default=True,
        ),
    ]
