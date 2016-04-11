##########################################################################
# Author: Daniel Kindimba
# Project: ScholarNet
##########################################################################
from django.conf.urls import include, url
from django.contrib import admin, auth
from . import views

urlpatterns = [
    ########################################################
    # Url for Mobile login
    #########################################################
    url(r'^login/$', views.login, name='login'),

    ##########################################################
    # url for user registration using the mobile devices
    ###########################################################
    url(r'^register/$', views.register, name='register'),


    ###########################################################
    # Url for resseting the password
    url(r'^passwordResset/$', views.passwordResset, name='passwordResset'),

    ##########################################################
    # Url for returning the List of Institutes in List Json format
    #########################################################
    url(r'^instituteList/$', views.instituteList, name='instituteList'),

    ############################################################
    # Url for returning the courses list regarding the Institutes
    #############################################################
    url(r'^courseList/$', views.courseList, name='courseList'),

    ############################################################################
    # Url for returning the user Subject List regarding the user course of study
    #############################################################################
    url(r'^userSubjectList/$', views.userSubjectList, name='userSubjectList'),

    #############################################################################
    # Url for returning the list of Posts Per subject
    ############################################################################
    url(r'^postSubjectList/$', views.postSubjectList, name='postSubjectList'),

    #############################################################################
    # Url for retreiving all the comments of the post
    #############################################################################
    url(r'^getPostComments/$', views.getPostComments, name='getPostComments'),

    ##############################################################################
    # Url for getting all the post images
    ##############################################################################
    url(r'^getPostImages/$', views.getPostImages, name='getPostImages'),


    ##############################################################################
    # Url for Publishing the Post Comment
    ##############################################################################
    url(r'^setPostComment/$', views.setPostComment, name='setPostComment'),


    ##############################################################################
    # url for getting the user Display Name
    ##############################################################################
    url(r'^getDisplayName/$', views.getDisplayName, name='getDisplayName'),


    ##############################################################################
    # Url for registering a new post
    ##############################################################################
    url(r'^setPost/$', views.setPost, name='setPost'),


    ##############################################################################
    # Url for uploading image
    ##############################################################################
    url(r'^setImage/$', views.setImage, name='setImage'),

    ##############################################################################
    # Url for getting total comments
    ##############################################################################
    url(r'^getTotalComRecCount/$', views.getTotalComRecCount, name='getTotalComRecCount'),


    ###########################################################################################
    # Url for setting the post recommendations
    ###########################################################################################
    url(r'^setRecommendation/$', views.setRecommendation, name='setRecommendation'),


    ###########################################################################################
    # Url for deleting the post Article
    ############################################################################################
    url(r'^deletePost/$', views.deletePost, name='deletePost'),


    #############################################################################################
    # Url for updaitng the post
    ############################################################################################
    url(r'^updatePost/$', views.updatePost, name='updatePost'),


    ##########################################################################################################
    # Url for getting getRequestConirmationList
    ##########################################################################################################
    url(r'^getRequestConfirmationList/$', views.getRequestConfirmationList, name='getRequestConfirmationList'),



    ###########################################################################################################
    # url for reporting problmes for the mobile applications
    ###########################################################################################################
    url(r'^reportProblem/$', views.reportProblem, name='reportProblem'),


    ############################################################################################################
    # Url for setting the User Display Name
    ############################################################################################################
    url(r'^setDisplayName/$', views.setDisplayName, name='setDisplayName'),


    ############################################################################################################
    # url for setting the Year of study
    ############################################################################################################
    url(r'^setYear/$', views.setYear, name='setYear'),






    #############################################################################
    # Url for returning the list of users
    #############################################################################
    url(r'^usersList/$', views.usersList, name='usersList'),

        ]