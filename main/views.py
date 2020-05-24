from user.models import User
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from user.authentication import UserAuthentication
from user.permission import UserAccessPermission
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# ----------------------------------------------------------------
# -----------------GENERIC VIEWS----------------------------------
# ----------------------------------------------------------------

class BaseView(TemplateView,LoginRequiredMixin):
    login_url = '/user/login'
    template_name = 'home.html'

class MenuView(TemplateView,LoginRequiredMixin):
    model=User
    login_url = '/user/login'
    template_name = 'menu.html'

class NotificationView(TemplateView,LoginRequiredMixin):
    model = User
    login_url = '/user/login'
    template_name = 'notifications.html'

class MytimeslotsView(TemplateView,LoginRequiredMixin):
    model = User
    login_url = '/user/login'
    template_name = 'mytimeslots.html'

class ExploreView(TemplateView,LoginRequiredMixin):
    model = User
    login_url = '/user/login'
    template_name = 'shopsnearme.html'

class SlotsView(TemplateView,LoginRequiredMixin):
    model = User
    login_url = '/user/login'
    template_name = 'shopslots.html'


class TestView(APIView):
    """
    Returns home text if the user is authenticated successfully and has permissions.
    **Example requests**:
        GET /api/home/
    """

    authentication_classes = (UserAuthentication,)
    permission_classes = (UserAccessPermission,)

    def get(self, request):
        content = {
            'message': 'Welcome '
        }
        return Response(content, status=status.HTTP_200_OK)