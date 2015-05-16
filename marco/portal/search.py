from wagtail.wagtailsearch.index import get_indexed_models
from wagtail.wagtailsearch.backends import get_search_backend
from wagtail.wagtailcore.models import Page



query_string = request.GET.get('q', '')

# Search
if query_string != '': 
    s = get_search_backend()
    models = get_indexed_models()
    models.remove(Page)
    for item in models:
        results = s.search(query_string, item)
        for result in results:
            # need to filter based on url?

else:
    search_results = None