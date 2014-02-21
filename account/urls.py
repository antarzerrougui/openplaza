from django.conf.urls import patterns,url
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import RedirectView
from django.contrib.auth.urls import urlpatterns

from .views import *


urlpatterns += patterns('',
    url(r'^$', RedirectView.as_view(url = reverse_lazy("profile"))),
    url(r'^profile/$',login_required(Profile.as_view(template_name="registration/profile.html"),login_url =reverse_lazy('login') ), name="profile"),
    url(r'^register/',Register.as_view(template_name="registration/register.html"), name="register"),
)
