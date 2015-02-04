# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='portalimage',
            name='creator',
            field=models.CharField(max_length=255, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='portalimage',
            name='creator_URL',
            field=models.URLField(help_text=b'creator URL', blank=True),
            preserve_default=True,
        ),
    ]
