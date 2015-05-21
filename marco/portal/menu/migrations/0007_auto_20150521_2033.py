# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0006_menuentry_display_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='order',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='menuentry',
            name='display_options',
            field=models.CharField(default=b'A', max_length=1, choices=[(b'A', b'Always display'), (b'I', b'Display only to logged-in users'), (b'O', b'Display only to anonymous users')]),
            preserve_default=True,
        ),
    ]
