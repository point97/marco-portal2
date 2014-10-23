# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from wagtail.wagtailcore.models import Page

def create_ocean_stories_container(apps, schema_editor):
    # Get models
    ContentType = apps.get_model('contenttypes.ContentType')
    OceanStories = apps.get_model('ocean_stories.OceanStories')

    # Create content type for ocean_stories model
    ocean_stories_content_type, created = ContentType.objects.get_or_create(
        model='oceanstories', app_label='ocean_stories', defaults={'name': 'Ocean Stories'})

    # Find root page
    root_page = Page.objects.get(id=3)

    # Add child page
    child_page = OceanStories(
        title="Ocean Stories",
        slug='ocean-stories',
        live=False,
        content_type=ocean_stories_content_type,
    )
    root_page.add_child(instance=child_page)

class Migration(migrations.Migration):

    dependencies = [
        ('ocean_stories', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_ocean_stories_container),
    ]
