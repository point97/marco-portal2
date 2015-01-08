# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from wagtail.wagtailcore.models import Page

def create_initial_data(apps, schema_editor):
    home_page = Page.objects.get(url_path="/home/")
    ContentType = apps.get_model('contenttypes.ContentType')

    top_level_pages = [
        {'app': 'ocean_stories', 'model_name': 'OceanStories', 'title': 'Ocean Stories', 'content_type': 'oceanstories'},
        {'app': 'calendar', 'model_name': 'Calendar', 'title': 'Calendar', 'content_type': 'calendar'},
        {'app': 'data_gaps', 'model_name': 'DataGaps', 'title': 'Data Gaps', 'content_type': 'datagaps'},
        {'app': 'data_catalog', 'model_name': 'DataCatalog', 'title': 'Data Catalog', 'content_type': 'datacatalog'},
    ]

    for p in top_level_pages:
        model = apps.get_model('%s.%s' % (p['app'], p['model_name']))
        content_type, created = ContentType.objects.get_or_create(
            model=p['content_type'], app_label=p['app'])
        home_page.add_child(instance=model(
            title=p['title'],
            live=False,
            content_type=content_type,
        ))


class Migration(migrations.Migration):

    dependencies = [
        ('ocean_stories', '0001_initial'),
        ('calendar', '0001_initial'),
        ('data_gaps', '0001_initial'),
        ('data_catalog', '0001_initial'),
        ('home', '0001_initial'),
    
    ]

    operations = [
        migrations.RunPython(create_initial_data),
    ]
