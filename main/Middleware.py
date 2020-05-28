from django.shortcuts import redirect,reverse
from django.utils.deprecation import MiddlewareMixin

class RedirectAuthenticatedUsersFromHomePage(MiddlewareMixin):
    def process_request(self, request):
        if request.path=='/' and request.user.is_authenticated:
            return redirect(reverse('main:menu'))