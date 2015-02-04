# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20150122_2113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portalimage',
            name='creator_URL',
            field=models.URLField(blank=True),
            preserve_default=True,
        ),
    ]
