# custom_middleware.py

from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse

class AccessControlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # List of URLs that don't require privilege checks
        exempt_urls = [
            reverse('login'),  # Replace 'login' with the name of your login view URL
            reverse('register_user'),
            reverse('logout'),
            reverse('unauthorised_page'),  # A page to send unauthorised people to.
            # Add more exempt URLs as needed
        ]

        # If the user is not logged in
        if not request.user.is_authenticated:
            # Check if the requested URL is in the exempt URLs list
            if not any(request.path_info.startswith(url) for url in exempt_urls):
                # Redirect unauthenticated users to the login page
                return HttpResponseRedirect(reverse('login'))  # Replace 'login' with the actual login URL name

        # If the user is authenticated but doesn't have the required permission
        elif not request.user.has_perm('approved_user'):
            # Check if the requested URL is in the exempt URLs list
            if not any(request.path_info.startswith(url) for url in exempt_urls):
                # Redirect authenticated users without the special permission to a static page
                return HttpResponseRedirect(reverse('unauthorised_page'))  # Replace with your static page URL

        return None
