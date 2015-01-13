# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_page_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='description',
            field=wagtail.wagtailcore.fields.RichTextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
