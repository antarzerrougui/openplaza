from django.conf.urls import patterns, include, url

#from aliexpress import urls

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'plaza.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^account/', include('account.urls')),
    url(r'^aliexpress/', include('aliexpress.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
