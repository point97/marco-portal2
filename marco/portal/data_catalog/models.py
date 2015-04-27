from wagtail.wagtailcore.models import Page

from portal.base.models import PageBase
from views import theme_query

class DataCatalog(PageBase):
    subpage_types = []

    def get_context(self, request, *args, **kwargs):
    	return {
    		'self': self,
    		'request': request,
    		'themes': theme_query()
    	}
