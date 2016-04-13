from django.conf.urls import patterns, include, url
from . import settings
from django.contrib import admin
from app.forms import *
admin.autodiscover()
admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.site_title = settings.ADMIN_SITE_TITLE

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'scholarnet.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'', include('app.urls')),
    url(r'^app/', include('app.urls')),
    url(r'^mob/', include('mob.urls')),
    url(r'^web/', include('web.urls')),
    url(r'^manager/', include('manager.urls')),
    url(r'^likes/', include('likes.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'app.views.login', name='login'),
    # url(r'^login/$', 'django.contrib.auth.views.login',
    #     {"template_name": 'registration/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login',
        name='logout'),
    url(r'^user/password/reset/$', 'django.contrib.auth.views.password_reset',
        {'post_reset_redirect' : '/user/password/reset/done/',
         'password_reset_form': EmailValidationOnForgotPassword},
        name="password_reset"),
    url(r'^user/password/reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    url(r'^user/password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'post_reset_redirect' : '/user/password/done/'},name='password_reset_confirm'),
    url(r'^user/password/done/$', 'django.contrib.auth.views.password_reset_complete'),
)
