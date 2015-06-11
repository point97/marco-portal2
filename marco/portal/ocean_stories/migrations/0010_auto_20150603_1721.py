# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ocean_stories', '0009_oceanstorysection_map_legend'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oceanstorysection',
            name='map_legend',
            field=models.BooleanField(default=False, help_text=b"Check to display the map's legend to the right of the the section text."),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='oceanstorysection',
            name='media_embed_url',
            field=models.URLField(help_text=b"The URL to a video that you'd like to embed, e.g., https://vimeo.com/121095661. <br>To position this video before the text, set <em>Media position</em> to left, to position after, set <em>Media position</em> to right.", blank=True),
            preserve_default=True,
        ),
    ]
