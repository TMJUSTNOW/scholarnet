######################################################################################
# Author: Daniel Kindimba
# Project: ScholarNet
######################################################################################
from django.conf.urls import include, url
from django.contrib import admin, auth
from . import views

urlpatterns = [
    url(r'^$', views.home, name='manager'),
    url(r'^adminstrators/$', views.adminstrators, name='adminstrators'),
    url(r'^adminstratorsActivator/([a-z]+)/([0-9]+)/$',
        views.adminstratorsActivator, name='adminstratorsActivator'),
    url(r'^students/$', views.students, name='students'),
    url(r'^studentsActivator/([a-z]+)/([0-9]+)/$',
        views.studentsActivator, name='studentsActivator'),
    url(r'^educators/$', views.educators, name='educators'),
    url(r'^educatorsActivator/([a-z]+)/([0-9]+)/$',
        views.educatorsActivator, name='educatorActivator'),
    url(r'^deleteMember/([a-z]+)/([0-9]+)/$',
        views.deleteMember, name='deleteMember'),
    url(r'^schools/$', views.schools, name='schools'),
    url(r'^deleteSchool/([0-9]+)/$', views.deleteSchool, name='deleteSchool'),
    url(r'^editSchool/([0-9]+)/$', views.editSchool, name='editSchool'),

    #################################################################################
    # Url for Publishing Notifications to the users
    #################################################################################
    url(r'^notify/$', views.notify, name='notify'),



    url(r'^schoolsActivator/([a-z]+)/([0-9]+)/$',
        views.schoolsActivator, name='schoolsActivator'),
    url(r'^groups/$', views.groups, name='groups'),
    url(r'^deleteGroup/([0-9]+)/$',
        views.deleteGroup, name='deleteGroup'),
    url('^schoolCourses/([0-9]+)/$',
        views.schoolCourses, name='schoolCourses'),
    url(r'^courseSubjects/([0-9]+)/$',
        views.courseSubjects, name='courseSubjects'),
    url(r'^deleteCourseSubjects/([0-9]+)/$',
        views.deleteCourseSubjects, name='deleteCourseSubjects'),
    url(r'^courseSubjectsActivator/([a-z]+)/([0-9]+)/$',
        views.courseSubjectsActivator, name='courseSubjectsActivator'),
    url(r'^deleteCourse/([0-9]+)/$', views.deleteCourse, name='deleteCourse'),
    url(r'^courseActivator/([a-z]+)/([0-9]+)/$',
        views.courseActivator, name='courseActivator'),
    url(r'^feedbacks/([a-z]+)/$', views.feedbacks, name='feedbacks'),
    url(r'^editSubject/([0-9]+)/$', views.editSubject, name='editSubject'),

    url(r'^searchRelatedSubject/$', views.searchRelatedSubject, name='searchRelatedSubject'),
    url(r'^loadRelatedSubjectContent/([0-9]+)/$', views.loadRelatedSubjectContent, name='loadRelatedSubjectContent'),
        ]
