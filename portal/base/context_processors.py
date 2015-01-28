from django.conf import settings

def search_disabled(request):
    """Facility for disabling search functionality.

    This may be used in the future to automatically disable search if the search
    backend goes down.
    """
    return dict(SEARCH_DISABLED=False)
    # return dict(SEARCH_DISABLED=not settings.DEBUG)
