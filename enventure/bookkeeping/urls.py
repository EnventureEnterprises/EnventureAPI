
from . import views
from django.conf.urls import url, include

from django.contrib.auth.decorators import user_passes_test
from django.views.generic.base import TemplateView 

is_admin = user_passes_test(lambda u: u.is_superuser)


urlpatterns = [
      
]
