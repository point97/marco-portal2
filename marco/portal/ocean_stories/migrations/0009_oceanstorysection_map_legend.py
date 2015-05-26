# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ocean_stories', '0008_auto_20150203_2337'),
    ]

    operations = [
        migrations.AddField(
            model_name='oceanstorysection',
            name='map_legend',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
