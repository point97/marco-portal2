from wagtail.wagtailcore.models import Page

from django.http import HttpResponseRedirect
from portal.ocean_stories.models import OceanStory

class HomePage(Page):
    parent_page_types = []

    def serve(self, request):
        story = OceanStory.objects.live().order_by('?')[0]
        return HttpResponseRedirect(story.url)
