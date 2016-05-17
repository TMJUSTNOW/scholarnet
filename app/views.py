"""
Author: Daniel Kindimba
Project: ScholarNet
"""
from django.conf import settings
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpRequest, Http404, HttpResponseRedirect, HttpResponse, \
    HttpResponseBadRequest, HttpResponseNotAllowed
from endless_pagination.decorators import page_template
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import auth
from .forms import *
from django.contrib.auth.models import *
from django.forms import modelformset_factory
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json
import urllib
import random

"""
A function for striping all the html tags from the passed text
"""
def stripHTMLTags(html):
    """
    Strip HTML tags from any string and transfrom special entities
  """
    import re
    text = html

    # apply rules in given order!
    rules = [
        {r'>\s+': u'>'},  # remove spaces after a tag opens or closes
        {r'\s+': u' '},  # replace consecutive spaces
        {r'\s*<br\s*/?>\s*': u'\n'},  # newline after a <br>
        {r'</(div)\s*>\s*': u'\n'},  # newline after </p> and </div> and <h1/>...
        {r'</(p|h\d)\s*>\s*': u'\n\n'},  # newline after </p> and </div> and <h1/>...
        {r'<head>.*<\s*(/head|body)[^>]*>': u''},  # remove <head> to </head>
        {r'<a\s+href="([^"]+)"[^>]*>.*</a>': r'\1'},  # show links instead of texts
        {r'[ \t]*<[^<]*?/?>': u''},  # remove remaining tags
        {r'^\s+': u''}  # remove spaces at the beginning
    ]

    for rule in rules:
        for (k, v) in rule.items():
            regex = re.compile(k)
            text = regex.sub(v, text)

    # replace special strings
    special = {
        '&nbsp;': ' ', '&amp;': '&', '&quot;': '"',
        '&lt;': '<', '&gt;': '>'
    }

    for (k, v) in special.items():
        text = text.replace(k, v)

    return text


"""
Function for validing the Email -address , Return True or False
"""
def validatePhone(username):
    return True

def internationalizePhone(phone):
    if len(str(phone)) == 10:
        return '+255' + str(phone)[1:len(str(phone))]
    elif len(str(phone)) == 13 and str(phone)[0] == '+':
        return str(phone)
    elif len(str(phone)) == 12 and str(phone)[0] != '+':
        return '+' + str(phone)
    elif len(str(phone)) == 13 and str(phone)[0] != '+':
        part1 = str(phone)[:3]
        part2 = str(phone)[4:]
        return '+' + part1 + part2


"""
A function checking the Existence of the Phone number in the System
"""
def checkPhoneExistence(request):
    phone = internationalizePhone(request.GET.get('phone'))
    context = ''
    if User.objects.filter(username=phone).exists():
        context = 'true'
    else:
        context = 'false'
    return HttpResponse(context)



"""
A function Returning the List of User Roles (Groups Names)
"""
def get_usergroup(request):
    if request.user.groups.all().exists():
        return Group.objects.get(id=request.user.groups.all())



"""
A function for getting fellow Members
"""
def getFellowMembers(request):
    course_id = []
    for ugroup in request.user.groups.all():
        if ugroup.name == 'Teacher':
            userRelatedCourse = TeacherSubject.objects.filter(user_id=request.user.id)
            for userRel in userRelatedCourse:
                course_id.append(userRel.subject.course.id)
        elif ugroup.name == 'Student':
            course_id.append(request.user.profile.course.id)
    members = UserProfile.objects.filter(course_id__in=course_id)
    return members


"""
A function for Getting User subjects for Teachers and Students
"""
def getUserSubjects(request):
    subjects = ''
    for ugroup in request.user.groups.all():
        if ugroup.name == 'Teacher':
            subjects_ids = []
            teacherSubjects = TeacherSubject.objects.filter(user_id=request.user.id)
            for tsubject in teacherSubjects:
                subjects_ids.append(tsubject.subject.id)
            subjects = Subjects.objects.filter(id__in=subjects_ids)
        elif ugroup.name == 'Student':
            subjects = Subjects.objects.filter(course_id=request.user.profile.course.id)
    return subjects



@login_required
def colors(request):
    colors= [{"name": "red", "code":"#f44336", "isLight": False},
             {"name":"pink","code":"#e91e63","isLight":False},
             {"name":"purple","code":"#9c27b0","isLight":False},
             {"name":"deep-purple","code":"#673ab7","isLight":False},
             {"name":"indigo","code":"#3f51b5","isLight":False},
             {"name":"blue","code":"#2196f3","isLight":False},
             {"name":"light-blue","code":"#03a9f4","isLight":False},
             {"name":"cyan","code":"#00bcd4","isLight":True},
             {"name":"teal","code":"#009688","isLight":True},
             {"name":"green","code":"#4caf50","isLight":True},
             {"name":"light-green","code":"#8bc34a","isLight":True},
             {"name":"lime","code":"#cddc39","isLight":True},
             {"name":"yellow","code":"#ffeb3b","isLight":True},
             {"name":"amber","code":"#ffc107","isLight":True},
             {"name":"orange","code":"#ff9800","isLight":True},
             {"name":"deep-orange","code":"#ff5722","isLight":True},
             {"name":"brown","code":"#795548","isLight":False},
             {"name":"grey","code":"#9e9e9e","isLight":True},
             {"name":"blue-grey","code":"#607d8b","isLight":False}]
    colorJson = json.dumps(colors)
    return colorJson



"""
A function which return the login View
"""
@csrf_exempt
def login(request):
    if request.method == 'POST':
        if User.objects.filter(username=request.POST.get('username')).count() > 0:
            username = request.POST.get('username')
        else:
            username = internationalizePhone(request.POST.get('username'))
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            content = []
            info = {}
            info = {
                "status": True,
            }
            content.append(info)
            return HttpResponse(json.dumps(content))

        else:
            content = []
            info = {}
            info = {
                "status": False,
            }
            content.append(info)
            return HttpResponse(json.dumps(content))
    else:
        context = {
        }
        return render(request, "registration/login.html", context)


"""
A function which allow user to recommend on different Posts
"""
def recommend(request, post_id):
    content = []
    if Likes.objects.filter(user_id=request.user.id).filter(description_id=post_id).count() == 0:
        recommend = Likes()
        recommend.description_id = post_id
        recommend.user_id = request.user.id
        recommend.save()
        if Likes.objects.filter(user_id=request.user.id, description_id=post_id).count() == 1:
            info = {}
            info = {
                "recommendation": Likes.objects.filter(description_id=post_id).count(),
                "faved": 1,
            }
            content.append(info)
        else:
            pass
    elif Likes.objects.filter(description_id=post_id, user=request.user).count() == 1:
        unrecommend = Likes.objects.get(Q(description_id=post_id) & Q(user_id=request.user.id))
        unrecommend.delete()
        info = {}
        info = {
            "recommendation": Likes.objects.filter(description_id=post_id).count(),
            "faved": 0,
        }
        content.append(info)
    return HttpResponse(json.dumps(content))


"""
A function handling the home page Content
"""
@login_required
@page_template('home/entry_home_article_page.html')
def home(request, template='home/index.html', extra_context=None):
    """
    Checking if the User has configured His/her Account
    """
    if request.user.is_superuser:
        return HttpResponseRedirect("/manager/")
    else:
        if request.user.profile.school_id != None:
            """
            getting all the subject ids of the current user
            """
            user_course_id = []
            if request.user.is_superuser:
                return HttpResponseRedirect("/manager/")
            else:
                user_course_id.append(request.user.profile.course_id)
                for ugroup in request.user.groups.all():
                    if ugroup.name == 'Teacher':
                        userRelatedCourses = TeacherSubject.objects.filter(user_id=request.user.id)
                        for userRel in userRelatedCourses:
                            user_course_id.append(userRel.subject.course.id)
                    elif ugroup.name == 'Student':
                        userRelatedCourses = Courses.objects.filter(
                            course_category_id=request.user.profile.course.course_category_id,
                            level_id=request.user.profile.course.level_id)
                        for userRel in userRelatedCourses:
                            user_course_id.append(userRel.id)
            subject_ids = []
            subs = getUserSubjects(request)
            for sub in subs:
                subject_ids.append(sub.id)

            ImageFormSet = modelformset_factory(Images, form=ImageForm, extra=4)

            postObject = Descriptions.objects.filter(subject_id__in=subject_ids).order_by('-updated')
            obj_dict = dict([(obj.id, obj) for obj in postObject])
            imageObject = Images.objects.filter(description__in=postObject)
            likesObject = Likes.objects.filter(description__in=postObject, user_id=request.user.id)
            commentsObject = DescriptionsComments.objects.filter(description__in=postObject).order_by('updated')
            relation_dict = {}
            likes_dict = {}
            comments_dict = {}
            for obj in imageObject:
                relation_dict.setdefault(obj.description_id, []).append(obj)
                for ob in likesObject:
                    likes_dict.setdefault(ob.description_id, []).append(ob)
            for id, related_items in relation_dict.items():
                obj_dict[id].post_images = related_items
            for id, liked_items in likes_dict.items():
                obj_dict[id].faved = 'true'

            for obj in commentsObject:
                comments_dict.setdefault(obj.description_id, []).append(obj)
            for id, related_items in comments_dict.items():
                obj_dict[id].comment = related_items
            context = {
                'ugroup': get_usergroup(request),
                "subjects": getUserSubjects(request),
                "posts": postObject,
                "totalPost": Descriptions.objects.filter(subject_id__in=subject_ids).count(),
                "formset": ImageFormSet(queryset=Images.objects.none()),
                "members": getFellowMembers(request),
                "title": 'Home',
            }
            if extra_context is not None:
                context.update(extra_context)
            return render_to_response(template, context, context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect("/app/setup/")


"""
A function for Regneratin the Account Verification Code
"""
def verificationCodeRegenerate(request):
    if Recovery.objects.filter(phone=request.user.username, waiting=True).exists():
        if Recovery.objects.filter(phone=request.user.username, waiting=True).count() > 1:
            recoveryObject = Recovery.objects.filter(phone=request.user.username, waiting=True)
            for rec in recoveryObject:
                rec.delete()
        else:
            recoveryObject = Recovery.objects.get(Q(phone=request.user.username) and Q(waiting=True))
            recoveryObject.delete()
        #creating the New Recovery Code
        newRecoveryCode = Recovery()
        newRecoveryCode.phone = request.user.username
        newRecoveryCode.code = random.randint(1000, 9999)
        newRecoveryCode.waiting=False
        newRecoveryCode.save()
        content = []
        info = {}
        info = {
            "status": True,
            "message": "Activation Code Sent",
        }
        content.append(info)
        return HttpResponse(json.dumps(content))
    else:
        newRecoveryCode = Recovery()
        newRecoveryCode.phone = request.user.username
        newRecoveryCode.code = random.randint(1000, 9999)
        newRecoveryCode.waiting = False
        newRecoveryCode.save()
        content = []
        info = {}
        info = {
            "status": True,
            "message": "Activation Code Sent",
        }
        content.append(info)
        return HttpResponse(json.dumps(content))
    content = []
    info = {}
    info = {
        "status": False,
        "message": "Failed to Send Activation Code",
    }
    return HttpResponse(json.dumps(content))



"""
A function for Verifying the User Account
"""
@login_required
def accountVerify(request):
    code = request.GET.get('code')
    if Recovery.objects.filter(phone=request.user.username, waiting=True, code=code).exists():
        userObject = User.objects.get(id=request.user.id)
        userObject.is_active = True
        userObject.save()
        verifiedUser = User.objects.get(id=request.user.id)
        if verifiedUser.is_active:
            userProfile = UserProfile.objects.get(user_id=request.user.id)
            userProfile.config_state = 1
            userProfile.save()
        if Recovery.objects.filter(phone=request.user.username, waiting=True, code=code).count() > 1:
            recoveryObject = Recovery.objects.filter(phone=request.user.username, waiting=True, code=code)
            for rec in recoveryObject:
                rec.delete()
        else:
            recoveryObject = Recovery.objects.get(Q(phone=request.user.username) and Q(waiting=True) and Q(code=code))
            recoveryObject.delete()
        content = []
        info = {}
        info = {
            "status": True,
            "message": "Account Activated Successfully",
        }
        content.append(info)
        return HttpResponse(json.dumps(content))
    else:
        pass
    content = []
    info = {}
    info = {
        "status": False,
        "message": "Failed To Activate Account"
    }
    content.append(info)
    return HttpResponse(json.dumps(content))


"""
A function for handling the Profile Setup
"""
@login_required
def setup(request):
    if request.method == 'POST':
        if request.POST or None:
            userGroup = request.user.groups.all()
            uGroups = []
            for ug in userGroup:
                uGroups.append(ug.name)
            if 'Student' in uGroups:
                chuo = request.POST.get('chuo')
                course = request.POST.get('course')
                academic = request.POST.get('academic')
                year = request.POST.get('year')
                userProfileObject = UserProfile.objects.get(user_id=request.user.id)
                userProfileObject.school_id=chuo
                userProfileObject.course_id=course
                userProfileObject.academic_id = academic
                yearObject = Year.objects.get(code=year)
                userProfileObject.year_id=yearObject.id
                userProfileObject.config_state=2
                userProfileObject.save()
                if UserProfile.objects.filter(user_id=request.user.id,school_id=chuo,course_id=course,academic_id=academic,year_id=year).exists():
                    content = []
                    info = {}
                    info = {
                        "status": True,
                        "message": "Education Information Successfully Updated"
                    }
                    content.append(info)
                    return HttpResponse(json.dumps(content))
                else:
                    content = []
                    info = {}
                    info = {
                        "status": False,
                        "message": "Failed to Updated Education Information"
                    }
                    content.append(info)
                    return HttpResponse(json.dumps(content))
            elif 'Teacher' in uGroups:
                chuo = request.POST.get('chuo')
                course = request.POST.get('course')
                academic = request.POST.get('academic')
                year = request.POST.get('year')
                userProfileObject = UserProfile.objects.get(user_id=request.user.id)
                userProfileObject.school_id = chuo
                userProfileObject.course_id = course
                userProfileObject.academic_id = academic
                yearObject = Year.objects.get(code=year)
                userProfileObject.year_id = yearObject.id
                userProfileObject.config_state = 2
                userProfileObject.save()

                newTeacherSubjectObject = TeacherSubject()
                newTeacherSubjectObject.user_id = request.user.id
                newTeacherSubjectObject.subject_id = request.POST.get('subject')
                if TeacherSubject.objects.filter(user_id=request.user.id,
                                                 subject_id=request.POST.get('subject')).count() == 0:
                    newTeacherSubjectObject.save()
                content = []
                info = {}
                info = {
                    "status": True,
                    "message": "Education Information Successfully Updated"
                }
                content.append(info)
                return HttpResponse(json.dumps(content))
        else:
            pass
    else:
        vyuo = School.objects.all().exclude(is_active=False)
        context = {
            "vyuo": vyuo,
            "academicYears": AcademicYear.objects.all().exclude(is_active=False),
            "title": 'Account Setup',
        }
        return render(request, "home/setup.html", context)

"""
A function for handling the user profile
"""
@login_required
def profile(request):
    context = {
        "puser": User.objects.get(id=request.user.id),
    }
    return render(request, "home/profile.html", context)


"""
A function for Setting up the user Profile on Registration Progress
"""
@login_required
def profileSetup(request):
    if request.method == 'POST':
        if request.POST or None:
            user_pic = UserProfile.objects.get(user_id=request.user.id)
            if request.POST or None:
                user_pic.photo = request.FILES['pic']
                user_pic.display = request.POST.get('display')
                user_pic.config_state = 3
                user_pic.save()
                content = []
                info = {}
                info = {
                    "status": True,
                }
                content.append(info)
                return HttpResponse(json.dumps(content))
            else:
                content = []
                info = {}
                info = {
                    "status": False
                }
                content.append(info)
                return HttpResponse(json.dumps(content))
        else:
            content = []
            info = {}
            info = {
                "status": False
            }
            content.append(info)
            return HttpResponse(json.dumps(content))
    else:
        content = []
        info = {}
        info = {
            "status": False
        }
        content.append(info)
        return HttpResponse(json.dumps(content))


@login_required
def profilePic(request):
    if request.method == 'POST':
        user_pic = UserProfile.objects.get(user_id=request.user.id)
        user_pic.photo = request.FILES['pic']
        user_pic.save()

        newUserPic = UserProfile.objects.get(user_id=request.user.id)
        content = []
        info = {}
        info = {
            "status": True,
            "url": str(newUserPic.photo)
        }
        content.append(info)
        return HttpResponse(json.dumps(content))
    else:
        content = []
        info = {}
        info = {
            "status": False,
            "message": "Bad Request"
        }
        content.append(info)
        return HttpResponse(json.dumps(content))

"""
A fucntion for Getting the List  of School Search for Setup
"""
@login_required
def setupGetSchool(request):
    if request.method == 'POST':
        context = ''
        context += '<table class="table table-model-2 table-hover">'
        context += '<thead>'
        context += '<tr>'
        context += '<th>School Name</th>'
        context += '<th>Action</th>'
        context += '</tr>'
        context += '</thead>'

        context += '<tbody>'
        key = request.POST.get('search')
        schools = School.objects.filter(Q(name__icontains=key) | Q(code__icontains=key))
        if School.objects.filter(Q(name__icontains=key) | Q(code__icontains=key)).count() > 0:
            for school in schools:
                context += '<tr>'
                context += '<td>'+str(school.name)+' ('+str(school.code)+')</td>'
                context += '<td><a href="javascript:;" onclick="addSchool('+str(school.id)+\
                           ');" class="btn btn-green btn-sm pull-right">Add</a></td>'
                context += '</tr>'
        else:
            context += '<script>'
            context += 'alertify.warning("We can not Find it, Please Try again with another search keyword");'
            context += '</script>'

        context += '</tbody>'
        context += '</table>'
    else:
        context = '<div class="alert alert-danger text-center">Something Went Wrong</div>'
    return HttpResponse(context)



"""
A function for getting all the school for teacher Configuration page
"""
@csrf_exempt
@login_required
def setupGetSchoolTeacher(request):
    if request.method == 'POST':
        context = ''
        context += '<table class="table table-model-2 table-hover">'
        context += '<thead>'
        context += '<tr>'
        context += '<th>School Name</th>'
        context += '<th>Action</th>'
        context += '</tr>'
        context += '</thead>'

        context += '<tbody>'
        key = request.POST.get('searchTeachearSchool')
        schools = School.objects.filter(Q(name__icontains=key) | Q(code__icontains=key))
        if School.objects.filter(Q(name__icontains=key) | Q(code__icontains=key)).count() > 0:
            for school in schools:
                context += '<tr>'
                context += '<td>'+str(school.name)+' ('+str(school.code)+')</td>'
                context += '<td><a href="javascript:;" onclick="addSchoolTeacher('+str(school.id)+');" class="btn btn-green btn-sm pull-right">Add</a></td>'
                context += '</tr>'
        else:
            context += '<script>'
            context += 'alertify.warning("We can not Find it, Please Try again with another search keyword");'
            context += '</script>'

        context += '</tbody>'
        context += '</table>'
    else:
        context = '<div class="alert alert-danger text-center">Something Went Wrong</div>'
    return HttpResponse(context)

"""
A fucntion for Adding a School To user from the Setup page
"""
@login_required
def setupAddSchool(request, schoolId):
    userObject = UserProfile.objects.get(user_id=request.user.id)
    userObject.school_id=schoolId
    userObject.save()

    schoolObject = School.objects.get(id=schoolId)
    if UserProfile.objects.filter(user_id=request.user.id, school_id=schoolId).exists():
        messages.success(request, str(schoolObject.name) + ' Successfully Added')
    else:
        messages.error(request, str(schoolObject.name) + ' Failed to Add, please Try again')
    return HttpResponseRedirect("/app/setup/")




"""
A function for Adding a school to User for the Teacher in sthe setup page (Configurations)
"""
@login_required
def setupAddSchoolTeacher(request, schoolId):
    if request.user.profile.school_id == '':
        userObject = UserProfile.objects.get(user_id=request.user.id)
        userObject.school_id = schoolId
        userObject.save()
    else:
        teacherSchoolObject = TeacherSchool()
        teacherSchoolObject.user_id = request.user.id
        teacherSchoolObject.school_id = schoolId
        teacherSchoolObject.save()
    return HttpResponseRedirect("/app/setup/")


"""
A function for Deleting the Teacher Subject
"""
@login_required
def deleteTeacherSubject(request, subjectId):
    if TeacherSubject.objects.filter(id=subjectId, user_id=request.user.id).count() > 0:
        teacherSubjectObject = TeacherSubject.objects.get(id=subjectId)
        teacherSubjectObject.delete()
        if TeacherSubject.objects.filter(id=subjectId) == 0:
            messages.success(request, str(teacherSubjectObject.subject.name) + ' Successfully Deleted')
        else:
            messages.error(request, str(teacherSubjectObject.subject.name) + ' Deletion Failed')
    else:
        messages.warning(request, 'No subject')
    return HttpResponseRedirect("/app/setup/")


"""
A function for getting user subject list in the configuration page
"""
@login_required
def loadTeacherSubjectList(request):
    courseId = request.GET.get('courseId')
    academicId = request.GET.get('academicId')
    yearId = request.GET.get('yearId')
    yearObject = Year.objects.get(code=yearId)
    subjects = Subjects.objects.filter(course_id=courseId, year_id=yearObject.id)
    content = []
    for subject in subjects:
        info = {}
        info = {
            "id": subject.id,
            "subject": subject.name,
            "code": subject.code,
        }
        content.append(info)

    return HttpResponse(json.dumps(content))



"""
A function for Adding a subject
"""
@login_required
@csrf_exempt
def teacherAddSubject(request):
    if request.method == 'POST':
        school = request.POST.get('school')
        course = request.POST.get('course')
        academic = request.POST.get('academic')
        subject = request.POST.get('subject')
        year = request.POST.get('year')
        teacherSubject = TeacherSubject()
        teacherSubject.user_id = request.user.id
        teacherSubject.subject_id = subject
        if TeacherSubject.objects.filter(user_id=request.user.id, subject_id=subject).count() == 0:
            teacherSubject.save()


        """
        Getting the subject object
        """
        subjectObj  = Subjects.objects.get(id=subject)
        context = '<center><a href="javascript:;" onclick="addSubjectTeacherModal('+str(school)+');" ' \
                  'class="btn btn-green btn-lg">Add New</a></center>'
        if TeacherSubject.objects.filter(user_id=request.user.id, subject_id=subject).count() > 0:
            context += '<script>alertify.success('+str(subjectObj.name)+' " Successfully Added");</script>'
        else:
            context += '<script>alertify.error("Faield to Register "'+str(subjectObj.name)+');</script>'
    return HttpResponse(context)



"""
A function for Adding the Study Year
"""
@login_required
def setupAddStudyYear(request, yearId):
    userObject = UserProfile.objects.get(user_id=request.user.id)
    userObject.year_id = yearId
    userObject.save()

    yearObject = Year.objects.get(id=yearId)
    if UserProfile.objects.filter(user_id=request.user.id, year_id=yearId).exists():
        messages.success(request, str(yearObject.name) + ' Successfully Added')
    else:
        messages.error(request, str(yearObject.name) + ' Failed to Add, Please Try again')
    return HttpResponseRedirect("/app/setup/")


"""
A function for adding the Study Course for the setup page user configuration
"""
@login_required
def setupAddCourse(request, courseId):
    userObject = UserProfile.objects.get(user_id=request.user.id)
    userObject.course_id=courseId
    userObject.save()

    courseObject = Courses.objects.get(id=courseId)
    if UserProfile.objects.filter(user_id=request.user.id, course_id=courseId).exists():
        messages.success(request, str(courseObject.name) + ' Successfully Added')
    else:
        messages.error(request, str(courseObject.name) + ' Failed to Add')
    return HttpResponseRedirect("/app/setup/")



"""
A function for adding the Academic Year for the setup page user configuration
"""
@login_required
def setupAddAcademicYear(request, academicId):
    userObject = UserProfile.objects.get(user_id=request.user.id)
    userObject.academic_id = academicId
    userObject.save()

    academicObject = AcademicYear.objects.get(id=academicId)
    if UserProfile.objects.filter(user_id=request.user.id, academic_id=academicId).exists():
        messages.success(request, str(academicObject.name) + ' Successfully Added')
    else:
        messages.error(request, str(academicObject.name) + ' Faield to Add')

    return HttpResponseRedirect("/app/setup/")


"""
A function for searching Extra Post Related information from google
"""
@login_required
def extraInfos(request, post_id):
    context = ""
    context += '<div class="alert alert-warning"><center>There is no Related informations</center></div>'
    return HttpResponse(context)


"""
A Fucntion for Reading the Post Details
"""
@login_required
def reader(request, post_id):
    ImageFormSet = modelformset_factory(Images, form=ImageForm, extra=4)

    userCourseIds = []
    userRelatedCourses = Courses.objects.filter(course_category_id=request.user.profile.course.course_category_id)
    for ur in userRelatedCourses:
        userCourseIds.append(ur.id)
    subjectsObj = Subjects.objects.filter(course_id__in=userCourseIds)
    subjects_ids = []
    if Descriptions.objects.filter(id=post_id).count() > 0:
        postObject = Descriptions.objects.get(id=post_id)
        for subjectsO in subjectsObj:
            subjects_ids.append(subjectsO.id)
        if postObject.subject_id in subjects_ids:
            postObj = Descriptions.objects.get(id=post_id)
        else:
            return HttpResponseRedirect("/app/error/")
    else:
        return HttpResponseRedirect("/app/error/")


    postObject = Descriptions.objects.filter(id=post_id)
    obj_dict = dict([(obj.id, obj) for obj in postObject])
    imageObject = Images.objects.filter(description__in=postObject)
    relation_dict = {}
    for obj in imageObject:
        relation_dict.setdefault(obj.description_id, []).append(obj)
    for id, related_items in relation_dict.items():
        obj_dict[id].post_images = related_items
    context = {
        'ugroup': get_usergroup(request),
        "post_id": post_id,
        "postObj": postObj,
        "subjects": getUserSubjects(request),
        "posts": postObject,
        "formset": ImageFormSet(queryset=Images.objects.none()),
        "comments": DescriptionsComments.objects.filter(description_id=post_id).order_by('-updated')[:10],
        "totalComments": DescriptionsComments.objects.filter(description_id=post_id).count(),
        "members": getFellowMembers(request),
        "title": "Reader",
    }
    return render(request, "home/reader.html", context)


"""
A function for Retreiving partuclar Subjects Posts
"""
@login_required
@page_template('home/entry_home_article_page.html')
def subjectReader(request, subject_id, template='home/index.html', extra_context=None):
    ImageFormSet = modelformset_factory(Images, form=ImageForm, extra=4)
    #getting all subject_id in which user is studying
    subjects_ids = []
    for subjectsO in getUserSubjects(request):
        subjects_ids.append(subjectsO.id)
    if int(subject_id) in subjects_ids:
        subject = Subjects.objects.get(id=subject_id)
    else:
        return HttpResponseRedirect("/app/error/")

    postObject = Descriptions.objects.filter(subject_id=subject_id).order_by('-updated')
    obj_dict = dict([(obj.id, obj) for obj in postObject])
    imageObject = Images.objects.filter(description__in=postObject)
    likesObject = Likes.objects.filter(description__in=postObject, user_id=request.user.id)
    commentsObject = DescriptionsComments.objects.filter(description__in=postObject).order_by('-updated')
    relation_dict = {}
    likes_dict = {}
    comments_dict = {}
    for obj in imageObject:
        relation_dict.setdefault(obj.description_id, []).append(obj)
        for ob in likesObject:
            likes_dict.setdefault(ob.description_id, []).append(ob)
    for id, related_items in relation_dict.items():
        obj_dict[id].post_images = related_items
    for id, liked_items in likes_dict.items():
        obj_dict[id].faved = 'true'

    for obj in commentsObject:
        comments_dict.setdefault(obj.description_id, []).append(obj)
    for id, related_items in comments_dict.items():
        obj_dict[id].comment = related_items
    context = {
        "upgrop": get_usergroup(request),
        "subjects": getUserSubjects(request),
        "posts": postObject,
        "subject_name": subject.name,
        "totalPost": Descriptions.objects.filter(subject_id=subject_id).count(),
        "formset": ImageFormSet(queryset=Images.objects.none()),
        "members": getFellowMembers(request),
        "subjectObj": subject,
        "title": subject.name,
    }

    if extra_context is not None:
        context.update(extra_context)
    # return render(request, "home/subject_reader.html", context)
    return render_to_response(template, context, context_instance=RequestContext(request))



def fake(request):
    subjectsObj = Subjects.objects.filter(course_id=request.user.profile.course_id)
    subjects_ids = []
    for subjectsO in subjectsObj:
        subjects_ids.append(subjectsO.id)
    context = {
        "upgrop": get_usergroup(request),
        "subjects": getUserSubjects(request),
        "members": getFellowMembers(request),
        "subjectObj": subjects_ids,
        "title": "Wrong Access",
    }
    return render(request, "home/fake_data.html", context)

"""
A function for retreveing List of users using ScholarNet, Exculding the Super User(Adminstrator of the System)
"""
@login_required
def users(request):
    context = {
        'ugroup': get_usergroup(request),
        "users": User.objects.all().exclude(is_superuser=True),
        "title": 'Users',
    }
    return render(request, "home/user_list.html", context)



"""
A function for returning the Institues List (All Institues/Schools)
"""
@login_required
def institutes(request):
    context = {
        'ugroup': get_usergroup(request),
        "institutes": School.objects.all().exclude(is_active=False),
        "title": 'Institutes',
    }
    return render(request, 'home/institute_list.html', context)




"""
A function for Registering Courses for a particular Institute/School
"""
@login_required
def registerCourse(request, school_id):
    if request.method == 'POST':
        if request.POST or None:
            course = Courses()
            course.name = request.POST.get('name')
            course.code = request.POST.get('code')
            course.school = School.objects.get(id=school_id)
            course.save()
            return HttpResponseRedirect("/app/institutes/")
        else:
            pass
    else:
        pass
    context = {
        'ugroup': get_usergroup(request),
        "years": Year.objects.all(),
        "title": 'Institutes',
    }
    return render(request, 'home/add_course.html', context)


"""
A function for registering the Institues to the ScholarNet System
"""
@login_required
def registerInstitute(request):
    form = SchoolRegistration()
    if request.method == 'POST':
        inst_form = SchoolRegistration(data=request.POST)
        if request.POST or None:
            if inst_form.is_valid():
                inst_form.save()
                return HttpResponseRedirect("/app/institutes/")
            else:
                form = SchoolRegistration(data=request.POST)
                pass
        else:
            pass
    else:
        pass

    context = {
        'ugroup': get_usergroup(request),
        "instForm": form,
        "title": 'Register Institute',
    }
    return render(request, 'home/register_institute.html', context)


"""
A function Returning the Courses List Regarding the School/Institue Id Passed
"""
@login_required
def coursesList(request, institute_id):
    context = {
        'ugroup': get_usergroup(request),
        "courses": Courses.objects.filter(school_id=institute_id),
        "title": 'Course List',
    }
    return render(request, "home/courses_list.html", context)


"""
 A function rEturning the courses list for The Account Setup Configuration
"""
@login_required
def setupCourseList(request):
    institute_id=request.GET.get('id')
    courses = Courses.objects.filter(school_id=institute_id).values('id', 'name', 'code')
    response = json.dumps([i for i in courses])
    return HttpResponse(response)


"""
A function Returning the Subject List Regarding the Course Id passed
"""
@login_required
def subjectList(request, course_id):
    institute = Courses.objects.get(id=course_id)
    context = {
        'ugroup': get_usergroup(request),
        "subjects": Subjects.objects.filter(course_id=course_id),
        "institute_id": institute.id,
        "title": 'Subject List',
    }
    return render(request, "home/subjects_list.html", context)


"""
A function for registering A subject Refering a Subject to a System
"""
@login_required
def registerSubject(request, course_id):
    course = Courses.objects.get(id=course_id)
    if request.method == 'POST':
        if request.POST or None:
            subject = Subjects()
            subject.name = request.POST.get('name')
            subject.code = request.POST.get('code')
            subject.year_id = request.POST.get('year')
            subject.course_id = course_id
            subject.save()
            return HttpResponseRedirect("/app/coursesList/" + str(course.school_id) + "/")
        else:
            pass
    else:
        pass
    context = {
        "ugroup": get_usergroup(request),
        "years": Year.objects.all(),
        "title": 'Register Subject',
    }
    return render(request, "home/add_subject.html", context)


"""
A function for Publishing a New Post
"""
@login_required
def postPublish(request):
    if request.method == 'POST':
        if request.POST or None:
            if request.POST or None:
                # creating the post object for post registration
                if Descriptions.objects.filter(subject_id=request.POST.get('subject'),
                                               description=request.POST.get('description')).count() < 1:
                    post = Descriptions()
                    post.subject_id = request.POST.get('subject')
                    post.description = stripHTMLTags(request.POST.get('description'))
                    post.user_id = request.user.id
                    post.save()

                # #getting the published post_id
                pub_post = Descriptions.objects.get(Q(subject_id=request.POST.get('subject'))
                                                    and Q(description=stripHTMLTags(request.POST.get('description'))))

                for upfile in request.FILES.getlist('files'):
                    newImage = Images()
                    newImage.description_id = pub_post.id
                    newImage.url = upfile
                    newImage.save()
                return HttpResponseRedirect("/home/")
            else:
                pass
        else:
            pass
    return HttpResponseRedirect("/home/")


"""
A function for Editing the post
"""
def editPost(request):
    content = []
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        article = request.POST.get('article')

        """
        Initializing the Object to be updated
        """
        articleObject = Descriptions.objects.get(id=post_id)
        articleObject.description = article
        articleObject.save()
        info = {}
        if Descriptions.objects.filter(id=post_id, description=article).exists():
            info = {
                "content": article,
                "updated": 1,
            }
        else:
            info = {
                "content": article,
                "updated": 0,
            }
    content.append(info)
    return HttpResponse(json.dumps(content))



"""
A function for Deleting a Post, where by Post Unique Identifier is Passed
"""
@login_required
def deletePost(request, post_id):
    """
    deleting all the images posted
    """
    content = []
    images = Images.objects.filter(description_id=post_id)
    for image in images:
        image.delete()

    # deleting the descriptions
    description = Descriptions.objects.get(id=post_id)
    description.delete()

    # deleting the likes of the post
    likes = Likes.objects.filter(description_id=post_id)
    for like in likes:
        like.delete()

    if Images.objects.filter(description_id=post_id).exists() and Likes.objects.filter(description_id=post_id).exists():
        info = {}
        info = {
            "post_id": post_id,
            "deleted": 0,
        }
        content.append(info)
    else:
        info = {}
        info = {
            "post_id": post_id,
            "deleted": 1,
        }
        content.append(info)

    return HttpResponse(json.dumps(content))


"""
A function Loading the User Upgrade Interface
"""
@login_required
def upgradeLoader(request):
    context = ""
    context += '<div class="form-group">'
    context += '<label>Institute</label>'
    context += '<select name="institute" class="form-control" required >'
    context += '<option value="">Please Select Institute...</option>'
    context += '</select>'
    context += '</div><div class="form-group">'
    context += '<label>Course</label>'
    context += '<select name="institute" class="form-control" required>'
    context += '<option value="">Please Select Course ...</option>'
    context += '</select>'
    context += '</div>'
    context += '<div class="form-group">'
    context += '<label>Year</label>'
    context += '<select name="year" class="form-control" required>'
    context += '<option value="">Please Select ...</option>'
    context += '</select>'
    context += '</div>'
    context += '<div class="form-group">'
    context += '<button type="submit" class="btn btn-success btn-icon btn-lg pull-right">'
    context += '<i class="fa fa-cloud-upload"></i>&nbsp;&nbsp;'
    context += 'UPGRADE'
    context += '</button>'
    context += '</div>'
    return HttpResponse(context)


"""
A fucntion for publishing a Post Comment
"""
@login_required
def publishComment(request):
    context = ''
    post_id = request.POST.get('post_id')
    comment = request.POST.get('comment')
    user_id = request.user.id

    commentObj = DescriptionsComments()
    commentObj.description_id = post_id
    commentObj.user_id = user_id
    commentObj.comment = comment
    content = []
    if DescriptionsComments.objects.filter(description_id=post_id, comment=comment, user_id=user_id).count() == 0:
        commentObj.save()
    else:
        pass
    if DescriptionsComments.objects.filter(description_id=post_id, comment=comment, user_id=user_id).count() > 0:
        commentObject = DescriptionsComments.objects.filter(description_id=post_id, comment=comment, user_id=user_id)
        for comment in commentObject:
            info = {}
            info = {
                "id": comment.id,
                "comment": comment.comment,
                "updated": str(comment.updated),
                "total_comments": DescriptionsComments.objects.filter(description_id=post_id).count(),
            }
            content.append(info)
    else:
        pass
    return HttpResponse(json.dumps(content))


"""
Url for laoding the Post Comments
"""
@login_required
def loadPostComments(request, post_id):
    context = ""
    postObj = Descriptions.objects.get(id=post_id)
    context += '<div class="row">'
    context += '<div class="col-sm-12">'
    context += '<div class="xe-widget xe-conversations">'
    context += '<div class="xe-header">'
    context += '<div class="xe-icon">'
    context += '<i class="linecons-comment"></i>'
    context += '</div>'
    context += '<div class="xe-label">'
    context += '<h3 class="text">'
    context += 'Comments <span class="badge badge-info">' + str(postObj.comments) + '</span>'
    context += '</h3>'
    context += '</div>'
    context += '</div>'
    if DescriptionsComments.objects.filter(description_id=post_id).count() > 0:
        context += '<div class="xe-body">'
        context += '<ul class="list-unstyled">'

        commentsList = DescriptionsComments.objects.filter(description_id=post_id).order_by('-updated')[:10]
        for comment in commentsList:
            context += '<li>'
            context += '<div class="xe-comment-entry">'
            context += '<a href="javascript:;" class="xe-user-img">'
            context += '<img src="/static/images/user.jpg" class="img-circle btn-green" width="40" />'
            context += '</a>'
            context += '<div class="xe-comment">'
            if request.user.id == comment.user.id:
                context += '<a href="javascript:;"'
                context += '" data-toggle="tooltip" data-placement="top" title="Delete" onclick="deleteMe(' + str(
                    comment.id) + ');" class="pull-right">'
                context += '<i class="fa fa-trash"></i>'
                context += '</a>'
            context += '<a href="javascript:;" class="xe-user-name">'
            context += '<strong>' + str(comment.user.profile.display) + '</strong>'
            context += '</a>'
            context += '<p>' + str(comment.comment) + '</p>'
            context += '<span class="pull-right badge badge-gray">'
            context += str(comment.updated)
            context += '</span>'
            context += '</div>'
            context += '</div>'
            context += '</li>'

        context += '</ul>'
        context += '</div>'
    else:
        context += '<div>'
        context += '<center><h3>No Comments Found...</h3></center>'
        context += '</div>'
    if DescriptionsComments.objects.filter(description_id=post_id).count() > 10:
        context += '<div class="xe-footer">'
        context += '<a href="javascript:;" onclick="viewMoreComments(' + str(
            post_id) + ');" data-toggle="modal" data-target="#viewComments">View All</a>'
        context += '</div>'
    context += '</div>'
    context += '</div>'
    context += '</div>'
    return HttpResponse(context)


"""
A fuction for Viewing All the Comments
"""
@login_required
def loadAllPostComments(request, post_id):
    context = ""
    postObj = Descriptions.objects.get(id=post_id)
    context += '<div class="row">'
    context += '<div class="col-sm-12">'
    context += '<div class="xe-widget xe-conversations">'
    context += '<div class="xe-header">'
    context += '<div class="xe-icon">'
    context += '<i class="linecons-comment"></i>'
    context += '</div>'
    context += '<div class="xe-label">'
    context += '<h3 class="text">'
    context += 'Comments <span class="badge badge-info">' + str(postObj.comments) + '</span>'
    context += '</h3>'
    context += '</div>'
    context += '</div>'
    if DescriptionsComments.objects.filter(description_id=post_id).count() > 0:
        context += '<div class="xe-body">'
        context += '<ul class="list-unstyled">'

        comments = DescriptionsComments.objects.filter(description_id=post_id).order_by('-updated')[10:]
        for comment in comments:
            context += '<li>'
            context += '<div class="xe-comment-entry">'
            context += '<a href="javascript:;" class="xe-user-img">'
            context += '<img src="/static/images/user.jpg" class="img-circle btn-green" width="40" />'
            context += '</a>'
            context += '<div class="xe-comment">'
            if request.user.id == comment.user.id:
                context += '<a href="javascript:;"'
                context += '" data-toggle="tooltip" data-placement="top" title="Delete" onclick="deleteMeFromAll(' + str(
                    comment.id) + ',' + str(post_id) + ');" class="pull-right">'
                context += '<i class="fa fa-trash"></i>'
                context += '</a>'
            context += '<a href="javascript:;" class="xe-user-name">'
            context += '<strong>' + str(comment.user.profile.display) + '</strong>'
            context += '</a>'
            context += '<p>' + str(comment.comment) + '</p>'
            context += '<span class="pull-right badge badge-gray">'
            context += str(comment.updated)
            context += '</span>'
            context += '</div>'
            context += '</div>'
            context += '</li>'

        context += '</ul>'
        context += '</div>'
    else:
        context += '<div>'
        context += '<center><h3>No Comments Found...</h3></center>'
        context += '</div>'
    context += '</div>'
    context += '</div>'
    context += '</div>'
    return HttpResponse(context)


"""
A function Handling User Registration
"""
def register(request):
    if request.method == 'POST':
        user_form = registration(data=request.POST)
        content = []
        if user_form.is_valid():
            user = User()
            user.username = internationalizePhone(request.POST.get('username'))
            user.set_password(request.POST.get('password'))
            user.is_active = False
            if User.objects.filter(username=internationalizePhone(request.POST.get('username'))).exists():
                info = {}
                info = {
                    "message": "Account Available",
                    "phone": internationalizePhone(request.POST.get('username')),
                    "status": False
                }
                content.append(info)
                return HttpResponse(json.dumps(content))
            else:
                user.save()
                role = request.POST.get('role')
                group = Group.objects.get(name=role)
                newUser = User.objects.get(username=internationalizePhone(request.POST.get('username')))
                newUser.groups.add(group)

                confirmationRequest = Recovery()
                confirmationRequest.phone = internationalizePhone(request.POST.get('username'))
                confirmationRequest.code = random.randint(1000, 10000)
                if Recovery.objects.filter(phone=internationalizePhone(request.POST.get('username'))).count() > 0:
                    oldRequest = Recovery.objects.get(phone=internationalizePhone(request.POST.get('username')))
                    oldRequest.delete()
                else:
                    pass
                confirmationRequest.save()

                if User.objects.filter(username=internationalizePhone(request.POST.get('username'))).exists():
                    info = {}
                    info = {
                        "message": "Successfully Registered",
                        "phone": internationalizePhone(request.POST.get('username')),
                        "status": True
                    }
                    content.append(info)
                    return HttpResponse(json.dumps(content))
                else:
                    info = {}
                    info = {
                        "message": "Failed To Register",
                        "phone": internationalizePhone(request.POST.get('username')),
                        "status": False
                    }
                    content.append(info)
                    return HttpResponse(json.dumps(content))
        else:
            info = {}
            info = {
                "message": "Invalid Data",
                "phone": internationalizePhone(request.POST.get('username')),
                "status": False
            }
            content.append(info)
            return HttpResponse(json.dumps(content))
    else:
        content = []
        info = {}
        info = {
            "message": "Bad Request",
            "status": False,
        }
        content.append(info)
        return HttpResponse(json.dumps(content))


"""
A function Handling User(Teachers) Registration
"""
def registerTeacher(request):
    if request.method == 'POST':
        user_form = registration(data=request.POST)
        if user_form.is_valid():
            user = User()
            user.username = internationalizePhone(request.POST.get('username'))
            user.set_password(request.POST.get('password'))
            user.is_active = False
            user.save()

            username = user_form.cleaned_data['username']
            if validatePhone(username):
                """
                updating the username if not registered
                """
                userName = User.objects.get(username=internationalizePhone(request.POST.get('username')))
                userName.username = internationalizePhone(request.POST.get('username'))
                userName.save()
                """
                Create and save user profile
                """
                new_user = User.objects.get(username=internationalizePhone(request.POST.get('username')))
                new_profile = UserProfile()
                new_profile.user_id = new_user.id
                new_profile.display = request.POST.get('display')
                new_profile.school_id = request.POST.get('institute')
                new_profile.course_id = request.POST.get('course')
                new_profile.year_id = request.POST.get('year')
                new_profile.save()


                role = request.POST.get('role')
                group = Group.objects.get(id=role)
                newUser = User.objects.get(username=internationalizePhone(request.POST.get('username')))
                newUser.groups.add(group)

                """
                Registering the registration confirmation request
                For the ScholarNet Message Service Responder to Process the requests
                """

                confirmationRequest = Recovery()
                confirmationRequest.phone = internationalizePhone(username)
                confirmationRequest.code = random.randint(1000, 10000)
                if Recovery.objects.filter(phone=internationalizePhone(username)).count() > 0:
                    oldRequest = Recovery.objects.get(phone=internationalizePhone(username))
                    oldRequest.delete()
                else:
                    pass
                confirmationRequest.save()

            else:
                new_user = User.objects.get(username=internationalizePhone(username))
                new_profile = UserProfile()
                new_profile.user_id = new_user.id
                new_profile.school_id = request.POST.get('institute')
                new_profile.course_id = request.POST.get('course')
                new_profile.year_id = request.POST.get('year')
                new_profile.save()

                role = request.GET.get('role')
                group = Group.objects.get(id=role)
                newUser.groups.add(group)

            if user:
                registeredUser = User.objects.get(username=internationalizePhone(request.POST.get('username')))
                if registeredUser.is_active == False:
                    return HttpResponseRedirect("/app/registrationConfiratiom/"+str(internationalizePhone(request.POST.get('username')))+"/")
                else:
                    return HttpResponseRedirect("/app/registerSuccess/")
            else:
                return HttpResponseRedirect("/app/registerFail/")
        else:
            context = {
                "title": "Registration",
                "form": user_form,
            }
            return render(request, 'registration/register.html', context)
    else:
        context = {
            "title": "Registration",
            "form": registration(),
            "years": Year.objects.all(),
            "groups": Group.objects.filter(name='Teacher'),
            "courses": Courses.objects.all().exclude(is_active=False),
            "institutes": School.objects.all().exclude(is_active=False),
        }
        return render(request, 'registration/register_teacher.html', context)


"""
A function for confirming the registration Process
"""
def registrationConfirm(request):
    if request.method == 'POST':
        phone = internationalizePhone(request.POST.get('phone'))
        code = request.POST.get('code')
        if Recovery.objects.filter(phone=phone, code=code, waiting=True).count() > 0:
            user = User.objects.get(username=phone)
            user.is_active = True
            user.save()
            activatedUser = User.objects.get(username=phone)
            if activatedUser.is_active:
                recoveryObjects = Recovery.objects.filter(phone=phone, code=code, waiting=True)
                for recoveryObject in recoveryObjects:
                    recoveryObject.delete()
                messages.success(request, str(activatedUser.username) + ' Successfully Activated')
                messages.success(request, 'You can now Login')
            else:
                messages.error(request, str(activatedUser.username) + ' Failed to Be activated')
                messages.info(request, 'Please Attempt to Register again')
        else:
            pass
    else:
        messages.error(request, 'Bad Request')
    return HttpResponseRedirect("/login/")

"""
A function for confirmining user registration process requiring to enter the received code in sms
"""
def registrationConfiratiom(request, phone):
    if request.method == 'POST':
        code = request.POST.get('code')
        phone = internationalizePhone(request.POST.get('phone'))
        if Recovery.objects.filter(phone=phone, code=code, waiting=True).count() > 0:
            recoveryObj = Recovery.objects.get(Q(phone=phone) & Q(code=code) & Q(waiting=True))
            userToConfirm = User.objects.get(username=recoveryObj.phone)
            userToConfirm.is_active = True
            userToConfirm.save()

            """
            Deleting the Confirmed User from the Confirmation Request
            """
            confirmedRequest = Recovery.objects.get(Q(phone=phone) & Q(code=code) & Q(waiting=True))
            confirmedRequest.delete()

            """
            User Object who is confirmed
            """
            confirmedUser = User.objects.get(username=recoveryObj.phone)
            if confirmedUser.is_active:
                return HttpResponseRedirect("/app/registerSuccess/")
            else:
                confirmationRequest = Recovery()
                confirmationRequest.phone = phone
                confirmationRequest.code = random.randint(1000, 10000)
                if Recovery.objects.filter(phone=phone).count() > 0:
                    oldRequest = Recovery.objects.get(phone=phone)
                    oldRequest.delete()
                else:
                    pass
                confirmationRequest.save()
                return HttpResponseRedirect("/app/registrationConfiratiom/"+str(phone)+"/")
    else:
        pass
    context = {
        "phone": phone,
    }
    return render(request, "registration/registration_confirm.html", context)



"""
A function for Resetting the User passwordd
"""
def passwordReset(request):
    if request.method == 'POST':
        phone = internationalizePhone(request.POST.get('phone'))
        if User.objects.filter(username=phone).count() > 0:
            if Recovery.objects.filter(phone=phone).count() > 0:
                oldRequest = Recovery.objects.filter(phone=phone)
                for old in oldRequest:
                    old.delete()
                newRequest = Recovery()
                newRequest.phone = phone
                newRequest.code = random.randint(1000, 10000)
                newRequest.save()
                context = {
                    "phone": phone,
                }
                return render(request, "registration/password_recovery_code.html", context)
            else:
                newRequest = Recovery()
                newRequest.phone = phone
                newRequest.code = random.randint(1000,10000)
                newRequest.save()
                context = {
                    "phone": phone,
                }
                return render(request, "registration/password_recovery_code.html", context)
        else:
            pass
    else:
        pass
    return HttpResponseRedirect("/user/password/reset/")




"""
A function for receiving and processing the password code confirmation
"""
def passwordCodeConfirm(request):
    if request.method == 'POST':
        phone = internationalizePhone(request.POST.get('phone'))
        code = request.POST.get('code')
        if Recovery.objects.filter(phone=phone, code=code, waiting=True).count() > 0:
            context = {
                "phone": phone,
            }
            return render(request, "registration/password_resseter_form.html", context)
        else:
            pass
    else:
        pass
    return HttpResponseRedirect("/user/password/reset/")




"""
A function for resetting the user password
"""
def passwordResseter(request):
    if request.method == 'POST':
        phone = internationalizePhone(request.POST.get('phone'))
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            user = User.objects.get(username=phone)
            user.set_password(password1)
            user.save()
            return HttpResponseRedirect("/login/")
        else:
            context = {
                "phone": phone,
            }
            return render(request, "registration/password_resseter_form.html", context)
    else:
        return HttpResponseRedirect("/login/")




"""
A function which laod List of courses in Ajax Call
"""
def loadCourses(request, institute_id):
    context = ""
    context += '<option value="">Please Select....</option>'
    courses = Courses.objects.filter(school_id=institute_id)
    for course in courses:
        context += '<option value="' + str(course.id) + '">' + course.name + '(' + course.code + ')' + '</option>'

    return HttpResponse(context)


"""
A function for deleting the Post Comment
"""
@login_required
def deleteComment(request, commentId):
    commentObj = DescriptionsComments.objects.get(id=commentId)
    post_id = commentObj.description_id
    commentObj.delete()
    response = ''
    response += '<script>'
    content = []
    if DescriptionsComments.objects.filter(id=commentId).count() == 0:
        info = {}
        info = {
            "id": commentId,
            "total_comment": DescriptionsComments.objects.filter(description_id=post_id).count(),
        }
        content.append(info)
    else:
        pass
    return HttpResponse(json.dumps(content))


"""
A function for loading the Institute Upgrade Form
"""
@login_required
@csrf_exempt
def upgradeInstituteLoadForm(request):
    context = ''
    context += '<form role="form" id="upgradeForm" action="/app/upgradeInstituteLoadForm/" method="POST">'

    context += '<div class="form-group">'
    context += '<label>Institute</label>'
    context += '<select name="institute" class="form-control" required>'
    context += '<option value="' + str(
        request.user.profile.school.id) + '">' + request.user.profile.school.name + '(' + request.user.profile.school.code + ')</option>'
    context += '</select>'
    context += '</div>'

    context += '<div class="form-group">'
    context += '<label>Course</label>'
    context += '<select name="course" class="form-control" required>'
    context += '<option value="' + str(
        request.user.profile.course.id) + '">' + request.user.profile.course.name + '(' + request.user.profile.course.code + ')</option>'
    context += '</select>'
    context += '</div>'

    context += '<div class="form-group">'
    context += '<label>Year</label>'
    context += '<select name="year" class="form-control" required">'
    context += '<option value="' + str(
        request.user.profile.year.id) + '">' + request.user.profile.year.name + '(' + str(
        request.user.profile.year.code) + ')</option>'
    context += '</select>'
    context += '</div>'

    context += '<div class="form-group">'
    context += '<button type="submit" class="btn btn-gray pull-right btn-lg">UPGRADE</button>'
    context += '</div>'

    context += '</form>'
    return HttpResponse(context)


"""
A function for loading the Course Upgrade Form
"""
@login_required
@csrf_exempt
def upgradeCourseLoadForm(request):
    if request.method == 'POST':
        course = request.POST.get('course')
        userYearObj = UserProfile.objects.get(user_id=request.user.id)
        userYearObj.course_id = course
        userYearObj.save()
        return HttpResponse('Successfully')
    else:
        context = ''
        context += '<form role="form" id="upgradeForm" action="/app/upgradeCourseLoadForm/" method="POST">'

        context += '<div class="form-group">'
        context += '<label>Course</label>'
        context += '<select name="course" class="form-control" required>'
        context += '<option value="' + str(
            request.user.profile.course.id) + '">' + request.user.profile.course.name + '</option>'
        coursesObj = Courses.objects.filter(school_id=request.user.profile.school.id).exclude(
            id=request.user.profile.course.id)
        for course in coursesObj:
            context += '<option value="' + str(course.id) + '">' + course.name + '</option>'
        context += '</select>'
        context += '</div>'

        context += '<div class="form-group">'
        context += '<button type="submit" class="btn btn-lg btn-gray pull-right">UPGRADE</button>'
        context += '</div>'
        context += '</form>'

        context += '<script>'
        context += '$("#upgradeForm").ajaxForm(function() {'
        context += 'var html = \'<center><img src="/static/images/ok.png" width="75" class="img img-responsive" /></center>\';'
        context += '$("#upgradeFormContainer").html(html);'
        context += 'alertify.success("Username Successfully updated");'
        context += '});'
        context += '</script>'
    return HttpResponse(context)




"""
A fucntion for loading the Year upgrade Form
"""
@login_required
@csrf_exempt
def upgradeDisplayNameLoadForm(request):
    if request.method == 'POST':
        display = request.POST.get('display')
        userProfObj = UserProfile.objects.get(user_id=request.user.id)
        userProfObj.display = display
        userProfObj.save()
        return HttpResponse('Upgraded')
    else:
        context = ''
        context += '<form role="form" action="/app/upgradeDisplayNameLoadForm/" method="POST" id="upgradeForm">'

        context += '<div class="form-group">'
        context += '<label>Display Name</label>'
        context += '<input type="text" name="display" class="form-control" required value="' + request.user.profile.display + '" />'
        context += '</div>'

        context += '<div class="form-group">'
        context += '<button type="submit"  class="btn btn-lg btn-gray pull-right">UPDATE</button>'
        context += '</div>'
        context += '</form>'
        context += '<script>'
        context += '$("#upgradeForm").ajaxForm(function() {'
        context += 'var html = \'<center><img src="/static/images/ok.png" width="75" class="img img-responsive" /></center>\';'
        context += '$("#upgradeFormContainer").html(html);'
        context += 'alertify.success("Username Successfully updated");'
        context += '});'
        context += '</script>'
        return HttpResponse(context)


"""
A function for upgrading the Year of study
"""
@login_required
@csrf_exempt
def upgradeYearLoadForm(request):
    if request.method == 'POST':
        year = request.POST.get('year')
        userYearObj = UserProfile.objects.get(user_id=request.user.id)
        userYearObj.year_id = year
        userYearObj.save()
        return HttpResponse('Successfully')
    else:
        context = ''
        context += '<form role="form" action="/app/upgradeYearLoadForm/" method="post" id="upgradeForm">'
        context += '<div class="form-group">'
        context += '<label>Year</label>'
        context += '<select name="year" class="form-control" required>'
        context += '<option value="' + str(
            request.user.profile.year.id) + '">' + request.user.profile.year.name + ' (' + str(
            request.user.profile.year.code) + ')</option>'
        yearObj = Year.objects.all().exclude(id=request.user.profile.year.id)
        for year in yearObj:
            context += '<option value="' + str(year.id) + '">' + year.name + '(' + str(year.code) + ')</option>'
        context += '</select>'
        context += '</div>'

        context += '<div class="form-group">'
        context += '<button type="submit" class="btn btn-lg btn-gray pull-right">UPGRADE</button>'
        context += '</div>'
        context += '</form>'
        context += '<script>'
        context += '$("#upgradeForm").ajaxForm(function() {'
        context += 'var html = \'<center><img src="/static/images/ok.png" width="75" class="img img-responsive" /></center>\';'
        context += '$("#upgradeFormContainer").html(html);'
        context += 'alertify.success("Year Successfully updated");'
        context += '});'
        context += '</script>'
        return HttpResponse(context)

"""
A function for returning the Success page for Successfully registration process
"""


def registerSuccess(request):
    context = {
        "message": "Your successfully registered",
    }
    return render(request, 'registration/success.html', context)


"""
A function for returning the Fail page for Un-Successfully Registration Process
"""


def registerFail(request):
    context = {
        "message": "We are Sorry, Registration Failed",
    }
    return render(request, 'registration/failure.html', context)


"""
A function for confirming the registered User
"""


def register_confirm(request, activation_key):
    """
    check if user is already logged in and if he is redirect him to some other url, e.g. home
    """
    if request.user.is_authenticated():
        HttpResponseRedirect('/home/')

    """
    check if there is UserProfile which matches the activation key (if not then display 404)
    """
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)

    """
    check if the activation key has expired, if it hase then render confirm_expired.html
    """
    if user_profile.key_expires < timezone.now():
        context = {
            "message": "We are sorry, Time for activation expired, please Register Again"
        }
        return render(request, 'registration/activation_expired.html', context)
    """
    if the key hasn't expired save user and set him as active and render some template to confirm activation
    """
    user = user_profile.user
    user.is_active = True
    activated = user.save()
    context = {
        "message": "Your account is Successfully Activated, Please login to proceed"
    }
    return render(request, 'registration/activation_success.html', context)


"""
A function for Managing User Feedbacks
"""


@login_required
@csrf_exempt
def feedbackManager(request):
    if request.method == 'POST':
        newFeedback = Feedback()
        newFeedback.user_id = request.user.id
        newFeedback.satisfaction = request.POST.get('satisfaction')
        newFeedback.features = request.POST.get('features')
        newFeedback.problems = request.POST.get('problems')
        newFeedback.addfeatures = request.POST.get('addfeatures')
        if request.POST.get('satisfaction') == '' and request.POST.get('features') == '' and request.POST.get(
                'problems') == '' and request.POST.get('addfeatures') == '':
            pass
        context = ''
        if request.POST.get('satisfaction') == '':
            context += '<script>feedbackForm();alertify.error("Please Fill atleast One Field");</script>'
        else:
            newFeedback.save()
            context = "<center><img src='/static/images/ok.png' class='img img-responsive'' /></center>"
            context += '<script>alertify.success("Feedback Successfully Submit");</script>'
    return HttpResponse(context)


"""
A function for searching the Institute ( University/College/School)
"""


@csrf_exempt
def instituteSearch(request):
    context = ''
    if request.method == 'POST':
        if request.POST or None:
            key = request.POST.get('instituteSearch')
            if key == '':
                context += '<div class="alert alert-info"><center>Please Write Something to Search</center></div>'
            else:
                context += '<ul class="list-group list-group-minimal">'
                schools = School.objects.filter(Q(name__icontains=key) | Q(code__icontains=key))
                if School.objects.filter(Q(name__icontains=key) | Q(code__icontains=key)).count() > 0:
                    for school in schools:
                        context += '<li class="list-group-item">'
                        context += '<i class="fa fa-check pull-right"></i>'
                        context += str(school.name) + '(' + str(school.code) + ')'
                        context += '<span class="badge badge-success">Registered</span>'
                else:
                    context += '<li class="list-group-item">'
                    context += '<a href="#" onclick="proposeNewInstitute();" data-toggle="tooltip" data-placement="top"' \
                               'title="Please Register" class="btn btn-success pull-right"><i class="fa fa-plus pull-right"></i></a>'
                    context += str(key)
                    context += '<span class="badge badge-danger">Un-registered</span>'

                context += '</li>'

                context += '</ul>'
        else:
            pass
    else:
        context += '<div class="alert alert-danger"><center>Something Went Wrong, Please Try again</center></div>'
    return HttpResponse(context)

"""
A function for Loading the Page for Managing the School/Institute/College/Univerity
"""
@login_required
def manageSchool(request):
    context = {
        'ugroup': get_usergroup(request),
        "subjects": Subjects.objects.filter(course_id=request.user.profile.course_id, year_id=request.user.profile.year_id),
        "members": getFellowMembers(request),
        "courses": Courses.objects.filter(school_id=request.user.profile.school_id),
        "categories": CourseCategory.objects.all().exclude(is_active=False),
        "levels": CourseLevel.objects.all().exclude(is_active=False),
        "title": "Manage",
    }
    return render(request, "home/manage_schools.html", context)

"""
A function for Getting lIs tof Courses Subjects To Manage
"""


@login_required
def getCoursesSubjectManage(request, courseId):
    context = ''
    context += '<ul class="list-group list-group-minimal">'
    subjectsObj = Subjects.objects.filter(course_id=courseId).order_by('year_id')
    if Subjects.objects.filter(course_id=courseId).count() > 0:
        for subject in subjectsObj:
            context += '<li class="list-group-item">'
            context += '<a href="javascript:;" data-id="' + str(
                subject.id) + '" data-toggle="modal" data-target="#editCourse" class="btn-link btn-xs pull-right subjectCourseEditBtn"><i class="fa fa-edit"></i></a>'
            context += '<a href="javascript:;" data-id="' + str(
                subject.id) + '" data-toggle="tooltip" data-placement="top" title="Delete Subject" class="btn-link btn-xs pull-right text-red deleteSubject"><i class="fa fa-trash"></i></a>'
            context += str(subject.name)
            context += '<span class="badge badge-info pull-left">' + str(subject.year.name) + '</span>'
            context += '</li>'
        context += '</ul>'
    else:
        context += '<div class="alert alert-info"><center>No Subject Register.... Please Register Subjects</center></div>'
    context += '<script>'
    context += '$(".deleteSubject").on(\'click\', function(){'
    context += 'var id = $(this).data("id");'
    context += 'swal({'
    context += 'title: "Are you sure?",'
    context += 'text: "Subject will be Deleted",'
    context += 'type: "warning",'
    context += 'showCancelButton: true,'
    context += 'confirmButtonColor: "#DD6B55",'
    context += 'confirmButtonText: "Yes, delete it!",'
    context += 'closeOnConfirm: true'
    context += '},'
    context += 'function(){'
    context += '$("#fakeLoader").load(\'/app/deleteSubjectMenage/\'+id+\'/\');'
    context += '});'
    context += '});'
    context += '$(".subjectCourseEditBtn").on(\'click\', function(){'
    context += 'var id = $(this).data("id");'
    context += '$("#editSubjectCourseFormContainer").load("/app/editCourseSubjectManageForm/"+id+"/");'
    context += '});'
    context += '</script>'
    return HttpResponse(context)

"""
A function To Add New Course
"""


@login_required
def addNewCourseManager(request):
    if request.method == 'POST':
        course = request.POST.get('course')
        code = request.POST.get('code')
        category = request.POST.get('category')
        level = request.POST.get('level')
        newCourse = Courses()
        if Courses.objects.filter(name=course, code=code, school_id=request.user.profile.school_id).count() == 0:
            newCourse.name = course
            newCourse.code = code
            newCourse.course_category_id = category
            newCourse.school_id = request.user.profile.school_id
            newCourse.level_id = level
            newCourse.save()
            if Courses.objects.filter(name=course, code=code, school_id=request.user.profile.school_id).count() > 0:
                response = '<script>alertify.success("Successfully Published");'
                response += '$("#newCourseContainer").'
                response += 'html("<center><img src=\'/static/images/ok.png\' class=\'img img-responsive\' width=\'125\' />");</script>'
            else:
                response = '<script>alertify.error("Failed");'
                response += '$("#newCourseContainer").'
                response += 'html("<center><img src=\'/static/images/remove.png\' class=\'img img-responsive\' width=\'125\' />");</script>'
        else:
            response = '<script>alertify.warning("Course allready Registered, Please register new Course");'
            response += '$("#newCourseContainer").'
            response += 'html("<center><img src=\'/static/images/warning.png\' class=\'img img-responsive\' width=\'125\' />");</script>'
    else:
        response = '<script>alertify.error("Bad Request...");</script>'
    return HttpResponse(response)


"""
A function for Deleting the Courses
"""
@login_required
def deleteCourseMenage(request, courseId):
    response = ''
    courseObj = Courses.objects.get(id=courseId)
    courseSubjectsObj = Subjects.objects.filter(course_id=courseId)
    # Deleting all the Subject Related with the Course
    for cs in courseSubjectsObj:
        cs.delete()
    # Deleting the Course
    courseObj.delete()
    response += '<script>'
    if Courses.objects.filter(id=courseId).count() == 0:
        response += 'alertify.success("Successfully Deleted");'
        response += 'setTimeout(reloader, 2000);'
    else:
        response += 'alertify.error("Failed to Delete");'
    response += '</script>'
    return HttpResponse(response)


@csrf_exempt
@login_required
def editCourseManageForm(request, courseId):
    if request.method == 'POST':
        name = request.POST.get('course')
        code = request.POST.get('code')
        category = request.POST.get('category')
        level = request.POST.get('level')
        courseObj = Courses.objects.get(id=courseId)
        courseObj.name = name
        courseObj.code = code
        courseObj.level_id = level
        courseObj.course_category_id = category
        courseObj.save()
        response = ''
        response = '<script>alertify.success("Successfully Updated");setTimeout(reloader, 2000);'
        response += '$("#courseEditForm").'
        response += 'html("<center><img src=\'/static/images/ok.png\' class=\'' \
                    'img img-responsive\' width=\'125\' />");</script>'
    else:
        courseObj = Courses.objects.get(id=courseId)
        response = ''
        response += '<form role="form" action="/app/editCourseManageForm/' + str(
            courseId) + '/" method="POST" id="editCourseFormAjax">'
        response += '<div class="form-group">'
        response += '<label>Course Name</label>'
        response += '<input type="text" name="course" class="form-control" value="' + str(
            courseObj.name) + '" required />'
        response += '</div>'
        response += '<div class="form-group">'
        response += '<label>Course Code</label>'
        response += '<input type="text" name="code" class="form-control" value="' + str(courseObj.code) + '" />'
        response += '</div>'

        response += '<div class="form-group">'
        response += '<label>Category</label>'
        response += '<select name="category" class="form-control" required>'
        if courseObj.course_category_id == None:
            response += '<option value="">Please Select ...</option>'
        else:
            response += '<option value="'+str(courseObj.course_category_id)+'">'+str(courseObj.course_category.name)+'</option>'
        categories = CourseCategory.objects.all().exclude(id=courseObj.course_category_id)
        for category in categories:
            response += '<option value="'+str(category.id)+'">'+str(category.name)+'</option>'
        response += '</select>'
        response += '</div>'

        response += '<div class="form-group">'
        response += '<label>Level</label>'
        response += '<select name="level" class="form-control" required>'
        if courseObj.level_id == None:
            response += '<option value="">Please Select ...</option>'
        else:
            response += '<option value="'+str(courseObj.level_id)+'">'+str(courseObj.level.name)+'</option>'
        levels = CourseLevel.objects.all().exclude(id=courseObj.level_id)
        for level in levels:
            response += '<option value="'+str(level.id)+'">'+str(level.name)+'</option>'
        response += '</select>'
        response += '</div>'
        response += '<div class="form-group">'
        response += '<button type="submit" class="btn btn-green btn-lg pull-right">Update</button>'
        response += '</div>'
        response += '</form>'
        response += '<script>'
        response += '$("#editCourseFormAjax").submit(function(e)'
        response += '{'
        response += 'var postData = $(this).serializeArray();'
        response += 'var formURL = $(this).attr("action");'
        response += '$.ajax('
        response += '{'
        response += 'url : formURL,'
        response += 'type: "POST",'
        response += 'data : postData,'
        response += 'success:function(data, textStatus, jqXHR)'
        response += '{'
        response += '$("#fakeLoader").html(data);'
        response += '},'
        response += 'error: function(jqXHR, textStatus, errorThrown)'
        response += '{'
        response += 'alertify.error(\'Something Went Wrong Try agian....\');'
        response += '}'
        response += '});'
        response += 'e.preventDefault();'
        response += '});'
        response += '</script>'

    return HttpResponse(response)


@csrf_exempt
@login_required
def addNewSubjectCourseManageForm(request, courseId):
    if request.method == 'POST':
        newSubject = Subjects()
        newSubject.name = request.POST.get('subject')
        newSubject.code = request.POST.get('code')
        newSubject.course_id = courseId
        newSubject.year_id = request.POST.get('year')
        newSubject.save()
        response = ''
        response = '<script>alertify.success("Successfully Registered");'
        response += '$("#newCourseSubjectForm").'
        response += 'html("<center><img src=\'/static/images/ok.png\' class=\'img img-responsive\' width=\'125\' />'
        response += '<br /><br /><br /><a href=\'javascript:;\' onclick=\'anotherSubject(' + str(
            courseId) + ');\' class=\'btn btn-info btn-lg \'>Add Another</a></center>");</script>'
    else:
        response = ''
        response += '<form role="form" action="/app/addNewSubjectCourseManageForm/' + str(
            courseId) + '/" method="POST" id="addNewSubjectCourseFormAjax">'
        response += '<div class="form-group">'
        response += '<label>Subject Name</label>'
        response += '<input type="text" name="subject" class="form-control" required />'
        response += '</div>'
        response += '<div class="form-group">'
        response += '<label>Subject Code</label>'
        response += '<input type="text" name="code" class="form-control" />'
        response += '</div>'
        response += '<div class="form-group">'
        response += '<label>Year</label>'
        response += '<select name="year" class="form-control" required>'
        response += '<option value="">Please Select ...</option>'
        years = Year.objects.all()
        for year in years:
            response += '<option value="' + str(year.id) + '">' + str(year.name) + '</option>'
        response += '</select>'
        response += '</div>'
        response += '<div class="form-group">'
        response += '<button type="submit" class="btn btn-green btn-lg pull-right">Save</button>'
        response += '</div>'
        response += '</form>'
        response += '<script>'
        response += '$("#addNewSubjectCourseFormAjax").submit(function(e)'
        response += '{'
        response += 'var postData = $(this).serializeArray();'
        response += 'var formURL = $(this).attr("action");'
        response += '$.ajax('
        response += '{'
        response += 'url : formURL,'
        response += 'type: "POST",'
        response += 'data : postData,'
        response += 'success:function(data, textStatus, jqXHR)'
        response += '{'
        response += '$("#fakeLoader").html(data);'
        response += '},'
        response += 'error: function(jqXHR, textStatus, errorThrown)'
        response += '{'
        response += 'alertify.error(\'Something Went Wrong Try agian....\');'
        response += '}'
        response += '});'
        response += 'e.preventDefault();'
        response += '});'
        response += '</script>'

    return HttpResponse(response)


@login_required
def deleteSubjectMenage(request, subjectId):
    subjectObj = Subjects.objects.get(id=subjectId)
    subjectObj.delete()
    response = '<script>alertify.success("Subject Successfully Deleted");setTimeout(reloader, 2000);</script>'
    return HttpResponse(response)


@csrf_exempt
@login_required
def editCourseSubjectManageForm(request, subjectId):
    if request.method == 'POST':
        subjectEdit = Subjects.objects.get(id=subjectId)
        subjectEdit.name = request.POST.get('subject')
        subjectEdit.code = request.POST.get('code')
        subjectEdit.year_id = request.POST.get('year')
        subjectEdit.save()
        response = ''
        response = '<script>alertify.success("Successfully Updated");setTimeout(reloader, 2000);'
        response += '$("#courseEditForm").'
        response += 'html("<center><img src=\'/static/images/ok.png\' class=\'img img-responsive\' width=\'125\' />");</script>'
    else:
        subjectObj = Subjects.objects.get(id=subjectId)
        response = ''
        response += '<form role="form" action="/app/editCourseSubjectManageForm/' + str(
            subjectId) + '/" method="POST" id="editCourseFormAjax">'
        response += '<div class="form-group">'
        response += '<label>Course Name</label>'
        response += '<input type="text" name="subject" class="form-control" value="' + str(
            subjectObj.name) + '" required />'
        response += '</div>'
        response += '<div class="form-group">'
        response += '<label>Course Code</label>'
        response += '<input type="text" name="code" class="form-control" value="' + str(subjectObj.code) + '" />'
        response += '</div>'
        response += '<div class="form-group">'
        response += '<label>Year</label>'
        response += '<select name="year" class="form-control" required>'
        response += '<option value="' + str(subjectObj.year.id) + '">' + str(subjectObj.year.name) + '</option>'
        years = Year.objects.all().exclude(id=subjectObj.year.id)
        for year in years:
            response += '<option value="' + str(year.id) + '">' + str(year.name) + '</option>'
        response += '</select>'
        response += '</div>'
        response += '<div class="form-group">'
        response += '<button type="submit" class="btn btn-green btn-lg pull-right">Update</button>'
        response += '</div>'
        response += '</form>'
        response += '<script>'
        response += '$("#editCourseFormAjax").submit(function(e)'
        response += '{'
        response += 'var postData = $(this).serializeArray();'
        response += 'var formURL = $(this).attr("action");'
        response += '$.ajax('
        response += '{'
        response += 'url : formURL,'
        response += 'type: "POST",'
        response += 'data : postData,'
        response += 'success:function(data, textStatus, jqXHR)'
        response += '{'
        response += '$("#fakeLoader").html(data);'
        response += '},'
        response += 'error: function(jqXHR, textStatus, errorThrown)'
        response += '{'
        response += 'alertify.error(\'Something Went Wrong Try agian....\');'
        response += '}'
        response += '});'
        response += 'e.preventDefault();'
        response += '});'
        response += '</script>'

    return HttpResponse(response)



@login_required
def linker(request):
    if request.user.profile.course.course_category_id != None:
        userCourseCategoryId = request.user.profile.course.course_category_id

    linkers = Courses.objects.filter(course_category_id=userCourseCategoryId,
                                     level_id=request.user.profile.course.level_id).exclude(id=request.user.profile.course.id).order_by("?")[:10]
    userGroups = request.user.groups.all()
    uGroups = []
    for ug in userGroups:
        uGroups.append(ug.name)

    user_ids = []
    course_ids = []
    if 'Student' in uGroups:
        course_ids.append(request.user.profile.course.id)
        for uCourse in Courses.objects.filter(course_category_id=request.user.profile.course.course_category_id,
                                              level_id=request.user.profile.course.level_id):
            course_ids.append(uCourse.id)
        for uid in UserProfile.objects.filter(course_id__in=course_ids).exclude(user_id=request.user.id):
            user_ids.append(uid.user_id)
    elif 'Teacher' in uGroups:
        pass
    context = {
        "upgrop": get_usergroup(request),
        "fusers": User.objects.filter(id__in=user_ids),
        "title": "Linker",
        "linkers": linkers,
    }
    return render(request, "home/linker.html", context)

@login_required
def getlinkerAction(request, schoolId):
    context = ''
    if SchoolLinker.objects.filter(school_id=schoolId).count() == 0:
        context += '<a href="javascript:;" onclick="linkMe('+str(schoolId)+');" data-id="2" data-toggle= "tooltip" '
        context += 'data-placement="top" title="Link/Connect Me"'
        context += 'class ="btn btn-green btn-sm pull-right linkMe" >'
        context += '<i class ="fa fa-link" > </i> Link'
        context += '</a>'
    else:
        context += '<a href="javascript:;" onclick="unlinkMe('+str(schoolId)+');" data-id="2" data-toggle= "tooltip" '
        context += 'data-placement="top" title="Link/Connect Me"'
        context += 'class ="btn btn-danger btn-sm pull-right UnlinkMe" >'
        context += '<i class ="fa fa-link" > </i> Un-Link'
        context += '</a>'
    return HttpResponse(context)

@login_required
def setLinker(request):
    content = []
    if request.method == 'GET' and 'user' in request.GET:
        userLinkerObject = UserLinker()
        userLinkerObject.user_id = request.user.id
        followUer = User.objects.get(id=request.GET.get('user'))
        userLinkerObject.follower = followUer
        if UserLinker.objects.filter(user_id=request.user.id, follower=request.GET.get('user')).count() == 0:
            userLinkerObject.save()
        if UserLinker.objects.filter(user_id=request.user.id, follower=followUer).count() > 0:
            info = {}
            info = {
                "status": True,
            }
            content.append(info)
        else:
            info = {}
            info = {
                "status": False
            }
            content.append(info)
    elif request.method == 'GET' and 'course' in request.GET:
        courseLinkerObject = CourseLinker()
        courseLinkerObject.user_id = request.user.id
        courseLinkerObject.course_id = request.GET.get('course')
        if CourseLinker.objects.filter(user_id=request.user.id, course_id=request.GET.get('course')).count() == 0:
            courseLinkerObject.save()
        if CourseLinker.objects.filter(user_id=request.user.id, course_id=request.GET.get('course')).count() > 0:
            info = {}
            info = {
                "status": True,
            }
            content.append(info)
        else:
            info = {}
            info = {
                "status": False,
            }
            content.append(info)
    elif request.method == 'GET' and 'school' in request.GET:
        schoolLinkerObject = SchoolLinker()
        schoolLinkerObject.user_id = request.user.id
        schoolLinkerObject.school_id = request.GET.get('school')
        if SchoolLinker.objects.filter(user_id=request.user.id, school_id=request.GET.get('school')).count() == 0:
            SchoolLinker.save()
        if SchoolLinker.objects.filter(user_id=request.user.id, school_id=request.GET.get('school')).count() > 0:
            info = {}
            info = {
                "status": True,
            }
            content.append(info)
        else:
            info = {}
            info = {
                "status": False,
            }
            content.append(info)
    else:
        info = {}
        info = {
            "status": False,
        }
        content.append(info)

    return HttpResponse(json.dumps(content))


@login_required
def sdrive(request):
    content=""
    return render(request, "home/sdrive.html", content)


@login_required
def settings(request):
    content = ""
    return render(request, "home/settings.html", content)
