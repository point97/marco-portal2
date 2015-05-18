# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_auto_20150122_2150'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='active',
            field=models.BooleanField(default=False, help_text=b'To display this menu, check this box. '),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='menu',
            name='footer',
            field=models.BooleanField(default=False, help_text=b'Select to display this menu in the footer rather than in the nav bar. (Only the first three menus will display.)'),
            preserve_default=True,
        ),
    ]
