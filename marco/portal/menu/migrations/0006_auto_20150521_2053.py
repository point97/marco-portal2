# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0005_auto_20150518_2309'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='menu',
            options={'ordering': ('footer', 'order')},
        ),
        migrations.AddField(
            model_name='menu',
            name='order',
            field=models.PositiveSmallIntegerField(default=1, help_text=b'The order that this menu appears. Lower numbers appear first.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='menuentry',
            name='display_options',
            field=models.CharField(default=b'A', max_length=1, choices=[(b'A', b'Always display'), (b'I', b'Display only to logged-in users'), (b'O', b'Display only to anonymous users')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='menu',
            name='footer',
            field=models.BooleanField(default=False, help_text=b'Select to display this menu in the footer rather than in the nav bar. The footer has enough room for four menus.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='menuentry',
            name='url',
            field=models.CharField(help_text=b'Note: URLs starting with http:// will open in a new window.', max_length=4096, null=True, blank=True),
            preserve_default=True,
        ),
    ]
