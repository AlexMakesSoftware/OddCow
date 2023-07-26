from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages


class AccessControlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # List of URLs that don't require privilege checks
        exempt_urls = [
            reverse('login'), 
            reverse('register_user'),
            reverse('logout'),
            reverse('unauthorised_page'),  # A page to send unauthorised people to.
        ]

        # If the user is not logged in
        if not request.user.is_authenticated:            
            # Check if the requested URL is in the exempt URLs list
            if not any(request.path_info.startswith(url) for url in exempt_urls):
                # Redirect unauthenticated users to the login page
                messages.info(request,"You need to login.")
                return HttpResponseRedirect(reverse('login'))

        # If the user is authenticated but doesn't have the required permission
        elif not request.user.has_perm('auth.approved_user'):
            # print("User authenticated but doesn't have approval.")            
            # Check if the requested URL is in the exempt URLs list
            if not any(request.path_info.startswith(url) for url in exempt_urls):
                # Redirect authenticated users without the special permission to a static page
                return HttpResponseRedirect(reverse('unauthorised_page')) 
        # else:
            # print("Authorised")
        return None
