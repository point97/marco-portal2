# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ocean_stories', '0010_auto_20150603_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='oceanstory',
            name='display_home_page',
            field=models.BooleanField(default=True, help_text=b'Check to display this ocean story on the home page'),
            preserve_default=True,
        ),
    ]
