##########################################################################
# Author: Daniel Kindimba
# Project: ScholarNet
##########################################################################
from django.conf.urls import include, url
from django.contrib import admin, auth
from . import views

urlpatterns = [
    url(r'login/$', views.login, name='login'),
    url(r'postList/$', views.postList, name='postList'),
        ]