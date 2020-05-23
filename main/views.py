from user.models import User
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

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


