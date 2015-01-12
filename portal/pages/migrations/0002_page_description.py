# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='description',
            field=wagtail.wagtailcore.fields.RichTextField(default='', blank=True),
            preserve_default=False,
        ),
    ]
