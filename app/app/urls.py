"""
Author: Daniel Kindimba
Project: ScholarNet
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin, auth
admin.autodiscover()
from . import views

urlpatterns = [
    #Base Url Loading the Login View Template
    url(r'^$', views.login, name='login'),

    #Uurl for Regenerating the Account Verification Code
    url(r'^verificationCodeRegenerate/$', views.verificationCodeRegenerate, name='verificationCodeRegenerate'),
    #Account Verification for the registered User
    url(r'^accountVerify/$', views.accountVerify, name='accountVerify'),
    # Url for Setting up the Profile
    url(r'^setup/$', views.setup, name='login'),
    #url for getting setupCourseList
    url(r'^setupCourseList/$', views.setupCourseList, name='setupCourseList'),
    #url for userProfile
    url(r'^profile/$', views.profile, name='profile'),
    #Url for Setting The User Profile
    url('^profileSetup/$', views.profileSetup, name='profileSetup'),
    #url for Setting The User Profile Picture
    url('^profilePic/$', views.profilePic, name='profilePic'),
    # Url for Getting the Search School for Setup Page
    url(r'^setupGetSchool/$', views.setupGetSchool, name='setupGetSchool'),
    # Url for getting  the school for Teacher configuration page
    url(r'^setupGetSchoolTeacher/$', views.setupGetSchoolTeacher, name='setupGetSchoolTeacher'),
    # Url for Adding the School from the Setup page
    url(r'^setupAddSchool/([0-9]+)/$', views.setupAddSchool, name='setupAddSchool'),
    # Url for Adding the School from the setup page for the Teacher
    url(r'^setupAddSchoolTeacher/([0-9]+)/$', views.setupAddSchoolTeacher, name='setupAddSchoolTeacher'),
    # Url for loading Subject list for Teacher Configuration
    url(r'^loadTeacherSubjectList/$', views.loadTeacherSubjectList, name='loadTeacherSubjectList'),
    # Url for Adding Subject for the Teacher in the Configuration Page
    url(r'^teacherAddSubject/$', views.teacherAddSubject, name='teacherAddSubject'),
    # Url for Deleting the Teacher subject in the configuration panel for teachers
    url(r'^deleteTeacherSubject/([0-9]+)/$', views.deleteTeacherSubject, name='deleteTeacherSubject'),
    # url for aDding the Study Year for Setup Page
    url(r'^setupAddStudyYear/([0-9]+)/$', views.setupAddStudyYear, name='setupAddStudyYear'),
    # url for Adding the Study Course for setup page
    url(r'^setupAddCourse/([0-9]+)/$', views.setupAddCourse, name='setupAddCourse'),
    # Url for Adding the Academic Year for the setup page
    url(r'^setupAddAcademicYear/([0-9]+)/$', views.setupAddAcademicYear, name='setupAddAcademicYear'),
    # Url for loading the home page After User has been loged in
    url(r'^home/$', views.home, name='home'),
    # Url for reading  List of Post Posted for a subject
    url(r'^subjectReader/([0-9]+)/$', views.subjectReader, name='subjectReader'),
    # Url for editting a post give an id
    url(r'^editPost/$', views.editPost, name='editPost'),
    # url for get Institutes/schools list
    url(r'^institutes/$', views.institutes, name='institutes'),
    # url for get Users List
    url(r'^users/$', views.users, name='users'),
    # Url for registering Institute/School to the system
    url(r'^registerInstitute/$', views.registerInstitute, name='registerInstitute'),
    # Url for registering Courses to the system
    url(r'^registerCourse/([0-9]+)/$', views.registerCourse, name='registerCourse'),
    # Url for Obtaining the list of courses
    url(r'^coursesList/([0-9]+)/$', views.coursesList, name='coursesList'),
    # Url for obtaining the List of Subjects
    url(r'subjectsList/([0-9]+)/$', views.subjectList, name='subjectsList'),
    # Url for registering Subject to the system
    url(r'^registerSubject/([0-9]+)/$', views.registerSubject, name='registerSubject'),
    # Url for gettting the List of Courses , Ajax loading
    url(r'^loadCourses/([0-9]+)/$', views.loadCourses, name='loadCourses'),
    # Url for Publishing the Post of the Subject Topic/Subtopic
    url(r'^postPublish/$', views.postPublish, name='postPublish'),
    # url for reading the Post content registering the Post Unique Identifier passed
    url(r'^reader/([0-9]+)/$', views.reader, name='reader'),
    # Url for Deleting the Post, Post Unique Identifie Passed
    url(r'^deletePost/([0-9]+)/$', views.deletePost, name='deletePost'),
    # Url for Recommending the Post
    url(r'^recommend/([0-9]+)/$', views.recommend, name='recommend'),
    # url for publishing the post comment
    url(r'^publishComment/$', views.publishComment, name='publishComment'),
    # Url for loading the Post comments
    url(r'^loadPostComments/([0-9]+)/$', views.loadPostComments, name='loadPostComments'),
    # Url for Loading all The Post Comments
    url(r'^loadAllPostComments/([0-9]+)/$', views.loadAllPostComments, name='loadAllPostComments'),
    # Url for deleting the Post comment
    url(r'^deleteComment/([0-9]+)/$', views.deleteComment, name='deleteComment'),
    # Url for loading the User Institute Upgrade Form
    url(r'^upgradeInstituteLoadForm/$', views.upgradeInstituteLoadForm, name='upgradeInstituteLoadForm'),
    # url for loading the User Course Upgrade Form
    url(r'^upgradeCourseLoadForm/$', views.upgradeCourseLoadForm, name='upgradeCourseLoadForm'),
    # Url for loading and Upgrading the Year of Study
    url(r'^upgradeYearLoadForm/$', views.upgradeYearLoadForm, name='upgradeYearLoadForm'),
    # Url for loading the Year Course Upgrade Form
    url(r'^upgradeDisplayNameLoadForm/$', views.upgradeDisplayNameLoadForm, name='upgradeDisplayNameLoadForm'),
    # url for User registration, this is for the web users
    url(r'^register/$', views.register, name='register'),
    # Url for Teacher Registration, this if  for th web users
    url(r'^registerTeacher/$', views.registerTeacher, name='registerTeacher'),
    # Url for Successfully registration feedback, loading the success page
    url(r'^registerSuccess/$', views.registerSuccess, name='registerSuccess'),
    # Url for Account Confiration After Registration
    url(r'^registrationConfiratiom/([0-9, +]+)/$', views.registrationConfiratiom, name='registrationConfiratiom'),
    # Url for loading the when the registration process failed
    url(r'^registerFail/$', views.registerFail, name='registerFail'),
    # url for Confirming the Registration by entering the sms code that was delivered
    url(r'^registrationConfirm/$', views.registrationConfirm, name='registrationConfirm'),
    # Url for resetting the password
    url(r'^passwordReset/$', views.passwordReset, name='passwordReset'),
    # Url for Processing the Passowrd REseeting
    url(r'^passwordResseter/$', views.passwordResseter, name='passwordResseter'),
    # Url for receving the password confirmation code
    url(r'^passwordCodeConfirm/$', views.passwordCodeConfirm, name='passwordCodeConfirm'),
    # Url for upgrading the Account
    url(r'^upgradeLoader/$', views.upgradeLoader, name='upgradeLoader'),
    # url for Searching Extra Post Rleated Information
    url(r'^extraInfos/([0-9]+)/$', views.extraInfos, name='extraInfos'),
    # url for Recording User Feedbacks
    url(r'^feedbackManager/$', views.feedbackManager, name='feedbackManager'),
    # Url for Searching the Institute
    url(r'^instituteSearch/$', views.instituteSearch, name='instituteSearch'),
    # Url for managing the schools  for School Adminstrator
    url(r'^manageSchool/$', views.manageSchool, name='manageSchool'),
    # url for getting course per course
    url(r'^getCoursesSubjectManage/([0-9]+)/$', views.getCoursesSubjectManage, name='getCoursesSubjectManage'),
    # Url for registering new course for school manager
    url(r'^addNewCourseManager/$', views.addNewCourseManager, name='addNewCourseManager'),
    # url for deleting the institute course manage
    url(r'^deleteCourseMenage/([0-9]+)/$', views.deleteCourseMenage, name='deleteCourseMenage'),
    # Url for Loading the Manage Course Edit form
    url(r'^editCourseManageForm/([0-9]+)/$', views.editCourseManageForm, name='editCourseManageForm'),
    # Url for loading the manage Subjec tCourse Registration form
    url(r'^addNewSubjectCourseManageForm/([0-9]+)/$', views.addNewSubjectCourseManageForm,
        name='addNewSubjectCourseManageForm'),
    # Url for deleting the subject for the School management
    url(r'^deleteSubjectMenage/([0-9]+)/$', views.deleteSubjectMenage, name='deleteSubjectMenage'),
    # Url for editing the subject Course for management (School Adminstrator)
    url(r'^editCourseSubjectManageForm/([0-9]+)/$', views.editCourseSubjectManageForm,
        name='editCourseSubjectManageForm'),
    # Url for users to link to other Schools/Colleges/Universities
    url(r'^linker/$', views.linker, name='linker'),
    # url for getting the linker action
    url(r'^getlinkerAction/([0-9]+)/$', views.getlinkerAction, name='getlinkerAction'),
    # Url for setting the Linker
    url(r'^setLinker/$', views.setLinker, name='setLinker'),



    #url for Accessing the Scholarnet Drive
    url(r'^sdrive/$', views.sdrive, name='sdrive'),


    #url for Setting of the Account
    url(r'^settings/$', views.settings, name='settings'),

    # Url for redidirecting a user if not allowed to acces data
    url(r'^error/$', views.fake, name='error'),

    url(r'^colors/$', views.colors, name='colors'),
    ]