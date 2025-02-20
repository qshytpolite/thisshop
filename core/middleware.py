from django.conf import settings
from django.urls import reverse

class SeparateSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request is for the admin interface
        if request.path.startswith(reverse('admin:index')):
            settings.SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
            settings.SESSION_COOKIE_NAME = 'admin_sessionid'
        else:
            # Default settings for shop users
            settings.SESSION_ENGINE = 'django.contrib.sessions.backends.db'
            settings.SESSION_COOKIE_NAME = 'shop_user_session'

        response = self.get_response(request)
        return response

    def process_response(self, request, response):
        return response