# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ocean_stories', '0003_oceanstory_feature_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='oceanstory',
            name='explore_title',
            field=models.CharField(max_length=256, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='oceanstory',
            name='explore_url',
            field=models.URLField(max_length=4096, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='oceanstory',
            name='hook',
            field=models.CharField(max_length=256, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='oceanstorysection',
            name='body',
            field=wagtail.wagtailcore.fields.RichTextField(blank=True),
            preserve_default=True,
        ),
    ]
