# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0004_make_focal_point_key_not_nullable'),
        ('data_gaps', '0002_auto_20141205_0024'),
    ]

    operations = [
        migrations.AddField(
            model_name='datagap',
            name='feature_image',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailimages.Image', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='datagap',
            name='target_year',
            field=models.CharField(default='', max_length=4),
            preserve_default=False,
        ),
    ]
