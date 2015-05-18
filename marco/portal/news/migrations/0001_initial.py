# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import modelcluster.fields
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_auto_20150122_2130'),
        ('wagtailcore', '0010_change_page_owner_to_null_on_delete'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('description', wagtail.wagtailcore.fields.RichTextField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('posted', models.DateField(help_text=b'Date story posted')),
                ('map_link', models.TextField(help_text=b"A Marine Planner map url, or blank if this story isn't connected to a map.", max_length=4096, null=True, blank=True)),
                ('description', wagtail.wagtailcore.fields.RichTextField(help_text=b"The article's introductory content. Text here appears in the list of news stories, as well as below the headline and above any section content in the story page.", null=True, blank=True)),
                ('feature_image', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='base.PortalImage', help_text=b'Image displayed on the news story list.', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='StorySection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(null=True, editable=False, blank=True)),
                ('media_embed_url', models.URLField(blank=True)),
                ('media_caption', models.CharField(max_length=255, blank=True)),
                ('media_position', models.CharField(default=b'left', max_length=8, choices=[(b'left', b'left'), (b'right', b'right'), (b'full', b'full')])),
                ('header', models.CharField(max_length=255, blank=True)),
                ('body', wagtail.wagtailcore.fields.RichTextField(blank=True)),
                ('media_image', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='base.PortalImage', null=True)),
                ('page', modelcluster.fields.ParentalKey(related_name='story_sections', to='news.Story')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
