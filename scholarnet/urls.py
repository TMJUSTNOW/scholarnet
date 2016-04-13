from django.conf.urls import patterns, include, url
from . import settings
from django.contrib import admin
from app.forms import *
from tastypie.api import Api
from web.api.resources import *
admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(UserResource())              # resource_name: user
v1_api.register(SchoolResource())            # resource_name : school
v1_api.register(YearResource())              # resource_name : year
v1_api.register(CourseCategoryResource())    # resource_name: courseCategory
v1_api.register(CourseLevelResource())       # resource_name: courseLevel
v1_api.register(AcademicYearResource())      # resource_name: academic
v1_api.register(CourseResource())            # resource_name: course
v1_api.register(SubjectResource())           # resource_name: subject
v1_api.register(SchoolLinkerResource())      # resource_name: linker
v1_api.register(DescriptionResource())       # resource_name: article
v1_api.register(DescriptionCommentResource())   # resource_name: comment
v1_api.register(LikeResource())                 # resource_name: like
v1_api.register(ImageResource())                # resource_name: image
v1_api.register(UserProfileResource())          # resource_name: profile
v1_api.register(NotificationResource())         # resource_name: notification
v1_api.register(RecoveryResource())             # resource_name: recovery



admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.site_title = settings.ADMIN_SITE_TITLE

urlpatterns = patterns('',
    url(r'^api/', include(v1_api.urls)),








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
