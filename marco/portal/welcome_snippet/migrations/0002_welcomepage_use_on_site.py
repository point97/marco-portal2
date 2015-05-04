# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('welcome_snippet', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='welcomepage',
            name='use_on_site',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
