from django.conf.urls import patterns,url
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import RedirectView

from .views import *

urlpatterns = patterns('',
    url(r'^get-token/$',GetTokenView.as_view(),name="aliexpress-get-token"),
    url(r'^auth/$',login_required(AuthView.as_view(template_name="aliexpress/auth.html"),login_url =reverse_lazy('login') ),name="aliexpress-auth"),
)
