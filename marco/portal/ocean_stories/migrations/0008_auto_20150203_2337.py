# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ocean_stories', '0007_auto_20150122_2225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oceanstorysection',
            name='media_embed_url',
            field=models.URLField(blank=True),
            preserve_default=True,
        ),
    ]
