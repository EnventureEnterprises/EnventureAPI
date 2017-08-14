__version__ = '1.0.4'
__all__ = (
    'View', 'GenericView', 'GenericModelView',
    'RedirectView', 'TemplateView', 'FormView',
    'ListView', 'DetailView', 'CreateView', 'UpdateView', 'DeleteView'
)

from django.views.generic import View
from django_vanilla.django_vanilla.views import (
    GenericView, RedirectView, TemplateView, FormView
)
from django_vanilla.django_vanilla.model_views import (
    GenericModelView, ListView, DetailView, CreateView, UpdateView, DeleteView
)
