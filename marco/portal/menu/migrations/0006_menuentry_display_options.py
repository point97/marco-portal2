# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0005_auto_20150518_2309'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuentry',
            name='display_options',
            field=models.CharField(default=b'A', max_length=1, choices=[(b'Always display', b'A'), (b'Display only to logged-in users', b'I'), (b'Display only to anonymous users', b'O')]),
            preserve_default=True,
        ),
    ]
