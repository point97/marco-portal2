# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ocean_stories', '0004_auto_20141219_2132'),
    ]

    operations = [
        migrations.AddField(
            model_name='oceanstories',
            name='description',
            field=wagtail.wagtailcore.fields.RichTextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='oceanstory',
            name='description',
            field=wagtail.wagtailcore.fields.RichTextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
