from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.core.urlresolvers import reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView

from users.views import UserViewSet
import bookkeeping
from oauth2_provider.views import AuthorizationView

from users.login import ConvertTokenView, TokenView, RevokeTokenView, invalidate_sessions

from bookkeeping import views



router = DefaultRouter()
router.register(r'users', UserViewSet)



urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/', include('authentication.urls')),
    url(r'^api/v1/', include(router.urls)),
    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter

    url(r'^api-root$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),
    url(r'^$', router.get_api_root_view(), name='backend-root'),

    
    url(r'^api/v1/entries',
        views.EntryEndpoint.as_view(), name='api-entry-index'),

    url(r'^api/v1/items',
        views.ItemEndpoint.as_view(), name='api-item-index'),

    url(r'^auth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^social_auth/', include('rest_framework_social_oauth2.urls')),


    url(r'^users/authorize/?$', AuthorizationView.as_view(), name="authorize"),
    url(r'^users/token/?$', TokenView.as_view(), name="token"),
    url(r'^users/convert-token/?$', ConvertTokenView.as_view(), name="convert_token"),
    url(r'^users/revoke-token/?$', RevokeTokenView.as_view(), name="revoke_token"),
    url(r'^users/invalidate-sessions/?$', invalidate_sessions, name="invalidate_sessions")



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
