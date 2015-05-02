# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailcore.fields
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('welcome_snippet', '0003_auto_20150501_1850'),
    ]

    operations = [
        migrations.AddField(
            model_name='welcomepageentry',
            name='description',
            field=wagtail.wagtailcore.fields.RichTextField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='welcomepageentry',
            name='welcome_page',
            field=modelcluster.fields.ParentalKey(related_name='entries', to='welcome_snippet.WelcomePage'),
            preserve_default=True,
        ),
    ]
