from user.models import User
from django.views.generic import TemplateView


# ----------------------------------------------------------------
# -----------------GENERIC VIEWS----------------------------------
# ----------------------------------------------------------------

class BaseView(TemplateView):
    template_name = 'home.html'

class MenuView(TemplateView):
    model=User
    template_name = 'menu.html'

class NotificationView(TemplateView):
    model = User
    template_name = 'notifications.html'

class MytimeslotsView(TemplateView):
    model = User
    template_name = 'mytimeslots.html'

class ExploreView(TemplateView):
    model = User
    template_name = 'shopsnearme.html'

class SlotsView(TemplateView):
    model = User
    template_name = 'shopslots.html'


