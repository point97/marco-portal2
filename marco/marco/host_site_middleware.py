from django.conf import settings
class HostSiteMiddleware:
    """Middleware to dynamically switch settings.SITE_ID based on the HTTP_HOST
    header used in the request.

    This is used _only_ to allow some of the models in data_manager to be
    displayed in a special "dev" site, which is used for group approval prior
    to being displayed on the "real" site. This approach is used rather than


    There are multiple technical issues with this approach, see
    https://code.djangoproject.com/ticket/15089 and elseware for discussions.

    Among other things, this is not a general solution for multitenancy in
    django. It may also not be compatible with future versions of django.
    """
    def process_request(self, request):
        name = request.META.get('HTTP_HOST')
        name = name.split(":")[0] # strip off the port number, if present
        from django.contrib.sites.models import Site
        try:
            s = Site.objects.get(domain=name)
            settings.SITE_ID = s.id
        except Site.DoesNotExist:
            pass

