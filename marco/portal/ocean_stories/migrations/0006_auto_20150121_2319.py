# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ocean_stories', '0005_auto_20150112_2302'),
        ('base', '__first__'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oceanstory',
            name='feature_image',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='base.PortalImage', null=True),
            preserve_default=True,
        ),
    ]
