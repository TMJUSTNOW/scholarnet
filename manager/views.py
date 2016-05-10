from django.conf import settings
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpRequest, Http404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from endless_pagination.decorators import page_template
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.models import *
from django.views.decorators.csrf import csrf_exempt
from pusher import Pusher
from app.models import *


@login_required
def notify(request):
    if request.method == 'POST':
        pusher = Pusher(
            app_id=str(settings.PUSHER_APP_ID),
            key=str(settings.PUSHER_KEY),
            secret=str(settings.PUSHER_SECRET)
        )
        pusher.trigger('test_channel', 'notification', {
            'message': 'First Notification',
        })
    context = {
        "title": 'Notification Manager',
    }
    return render(request, "manager/notification_manager.html", context)

@login_required
def message(request):
    context = ""
    return HttpResponse(context)


@login_required
def home(request):
    context = {
        "title": "Manager",
        "totalUsers": User.objects.all().count(),
        "totalEducators": User.objects.filter(groups__name='Educator').count(),
        "totalStudents": User.objects.filter(groups__name='Student').count(),
        "totalArticles": Descriptions.objects.all().count(),
        "totalSchools": School.objects.all().exclude(is_active=False).count(),
        "totalCourses": Courses.objects.all().count(),
        "totalSubjects": Subjects.objects.all().count(),
        "totalPhotos": Images.objects.all().count(),
        "totalRecommendations": Likes.objects.all().count(),
        "totalComments": DescriptionsComments.objects.all().count(),
    }
    return render(request, "manager/index.html", context)


@login_required
@page_template('manager/common/paginated_members.html')
def adminstrators(request, template='manager/members.html', extra_context=None):
    if request.method == 'GET' and 'key' in request.GET:
        key = request.GET.get('key')
        members = User.objects.filter(is_superuser=True).filter(username__icontains=key)
        if User.objects.filter(is_superuser=True).filter(username__icontains=key).exists():
            members = User.objects.filter(is_superuser=True).filter(username__icontains=key)
        elif UserProfile.objects.filter(display__icontains=key).exists():
            user_ids = []
            userProfileObject = UserProfile.objects.filter(display__icontains=key)
            for up in userProfileObject:
                user_ids.append(up.user.id)
            members = User.objects.filter(is_superuser=True).filter(id__in=user_ids)
        else:
            members = ''
    else:
        members = User.objects.filter(is_superuser=True)
    context = {
        "memberName": 'Adminstrators',
        "activatorSwitcher": 'adminstratorsActivator',
        "memberType": 'adminstrator',
        "members": members,
        "title": 'Adminstrators',
    }
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def adminstratorsActivator(request, key, adminstratorId):
    adminstratorObj = User.objects.get(id=adminstratorId)
    if key == 'activate':
        adminstratorObj.is_active = True
        adminstratorObj.save()
        activatedAdminstrator = User.objects.get(id=adminstratorId)
        if activatedAdminstrator.is_active:
            messages.success(request, activatedAdminstrator.username + " Successfully Activated")
        else:
            messages.error(request, "Activation Failed for " + activatedAdminstrator.username)
    elif key == 'deactivate':
        adminstratorObj.is_active = False
        adminstratorObj.save()
        deactivatedAdminstrator = User.objects.get(id=adminstratorId)
        if deactivatedAdminstrator.is_active:
            messages.error(request, "Deactivation Failed for " + deactivatedAdminstrator.username)
        else:
            messages.success(request, deactivatedAdminstrator.username + " Successfully Deactivated")
    return HttpResponseRedirect("/manager/adminstrators/")


@login_required
@page_template('manager/common/paginated_members.html')
def students(request, template='manager/members.html', extra_context=None):
    if request.method == 'GET' and 'key' in request.GET:
        key = request.GET.get('key')
        if User.objects.filter(groups__name='Student').filter(username__icontains=key).exists():
            members = User.objects.filter(groups__name='Student').filter(username__icontains=key)
        elif UserProfile.objects.filter(display__icontains=key).exists():
            user_ids = []
            userProfileObject = UserProfile.objects.filter(display__icontains=key)
            for up in userProfileObject:
                user_ids.append(up.user.id)
            members = User.objects.filter(groups__name='Student').filter(id__in=user_ids)
        else:
            members = ''
    else:
        members = User.objects.filter(groups__name='Student')
    context = {
        "memberName": 'Students',
        "activatorSwitcher": 'studentsActivator',
        "memberType": 'student',
        "members": members,
        "title": 'Students',
    }
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def studentsActivator(request, key,  studentId):
    studentObj = User.objects.get(id=studentId)
    if key == 'activate':
        studentObj.is_active = True
        studentObj.save()
        activatedStudent = User.objects.get(id=studentId)
        if activatedStudent.is_active:
            messages.success(request, activatedStudent.username + " Successfully Activated")
        else:
            messages.error(request, "Activation Failed For " + activatedStudent.username)
    elif key == 'deactivate':
        studentObj.is_active = False
        studentObj.save()
        deactivatedStudent = User.objects.get(id=studentId)
        if deactivatedStudent.is_active:
            messages.error(request, "Deactivation Failed for " + deactivatedStudent.username)
        else:
            messages.success(request, deactivatedStudent.username + " Deactivated")
    return HttpResponseRedirect("/manager/students/")


@login_required
@page_template('manager/common/paginated_members.html')
def educators(request, template='manager/members.html', extra_context=None):
    if request.method == 'GET' and 'key' in request.GET:
        key = request.GET.get('key')
        if User.objects.filter(Q(groups__name='Teacher') | Q(groups__name='Educator')).filter(username__icontains=key).exists():
            members = User.objects.filter(Q(groups__name='Teacher') | Q(groups__name='Educator')).filter(username__icontains=key)
        elif UserProfile.objects.filter(display__icontains=key).exists():
            userProfileObject = UserProfile.objects.filter(display__icontains=key)
            user_ids = []
            for up in userProfileObject:
                user_ids.append(up.user.id)
            members = User.objects.filter(Q(groups__name='Teacher') | Q(groups__name='Educator')).filter(id__in=user_ids)
        else:
            members = ''
    else:
        members = User.objects.filter(Q(groups__name='Teacher') | Q(groups__name='Educator'))
    context = {
        "memberName": 'Educators',
        "activatorSwitcher": 'educatorsActivator',
        "memberType": 'educator',
        "members": members,
        "title": 'Educators',
    }
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))



@login_required
def educatorsActivator(request, key, educatorId):
    educatorObj = User.objects.get(id=educatorId)
    if key == 'activate':
        educatorObj.is_active = True
        educatorObj.save()
        activatedEducator = User.objects.get(id=educatorId)
        if activatedEducator.is_active:
            messages.success(request, activatedEducator.username + " Successfully Activated")
        else:
            messages.error(request, "Activation Failed for " + activatedEducator.username)
    elif key == 'deactivate':
        educatorObj.is_active = False
        educatorObj.save()
        deactivatedEducator = User.objects.get(id=educatorId)
        if deactivatedEducator.is_active:
            messages.error(request, "Deactivation Failed for " + deactivatedEducator.username)
        else:
            messages.success(request, deactivatedEducator.username + " Successfully Deactivated")
    return HttpResponseRedirect("/manager/educators/")


@login_required
def deleteMember(request, memberType, memberId):
    if memberType == 'adminstrator':
        return HttpResponseRedirect("/manager/adminstrators/")
    elif memberType == 'student':
        return HttpResponseRedirect("/manager/students/")
    elif memberType == 'educator':
        return HttpResponseRedirect("/manager/educators/")
    else:
        pass


@login_required
@csrf_exempt
def schools(request):
    if request.method == 'POST':
        newSchool = School()
        newSchool.name = request.POST.get('school')
        newSchool.code = request.POST.get('code')
        if School.objects.filter(name=request.POST.get('school'), code=request.POST.get('code')).count() == 0:
            newSchool.save()
            if School.objects.filter(name=request.POST.get('school'), code=request.POST.get('code')).count() > 0:
                messages.success(request, str(request.POST.get('school')) + 'Successfully Registered')
            else:
                messages.error(request, str(request.POST.get('school')) + 'Failed to Register')
            return HttpResponseRedirect("/manager/schools/")
        else:
            messages.warning(request, str(request.POST.get('school')) + 'Allready Registered')
            return HttpResponseRedirect("/manager/schools/")
    if request.method == 'GET' and 'key' in request.GET:
        key = request.GET.get('key')
        schools = School.objects.filter(Q(name__icontains=key) | Q(code__icontains=key))
    else:
        schools = School.objects.all()
    context = {
        "schools": schools,
        "title": 'Schools',
    }
    return render(request, "manager/schools.html", context)

@login_required
def deleteSchool(request, schoolId):
    schoolObj = School.objects.get(id=schoolId)
    school_name = schoolObj.name
    courses = Courses.objects.filter(school_id=schoolId)
    for course in courses:
        subjects = Subjects.objects.filter(course_id=course.id)
        for subject in subjects:
            subject.delete()
        course.delete()
    schoolObj.delete()
    if School.objects.filter(id=shoolId).count() > 0:
        messages.success(request, str(school_name) + ' Successfully Deleted')
    else:
        messages.error(request, str(school_name) + ' Failed to be Deleted')
    return HttpResponseRedirect("/manager/schools/")

@login_required
def schoolsActivator(request, key, schoolId):
    schoolObj = School.objects.get(id=schoolId)
    if key == 'activate':
        schoolObj.is_active = True
        schoolObj.save()

        activatedSchool = School.objects.get(id=schoolId)
        if activatedSchool.is_active:
            messages.success(request, str(activatedSchool.name) + ' Successfully Activated')
        else:
            messages.error(request, str(activatedSchool.name) + ' Failed to Activate')
    elif key == 'deactivate':
        schoolObj.is_active = False
        schoolObj.save()

        deactivatedSchool = School.objects.get(id=schoolId)
        if deactivatedSchool.is_active:
            messages.error(request, str(deactivatedSchool.name) + ' Failed to Deactivated')
        else:
            messages.success(request, str(deactivatedSchool.name) + ' Successfully Activated')
    return HttpResponseRedirect("/manager/schools/")

@csrf_exempt
@login_required
def editSchool(request, schoolId):
    if request.method == 'POST':
        school = School.objects.get(id=schoolId)
        school.name = request.POST.get('school')
        school.code = request.POST.get('code')
        school.save()
        if School.objects.filter(name=request.POST.get('school'), code=request.POST.get('code')).count() > 0:
            messages.success(request, str(request.POST.get('school')) + ' Successfully Updated')
        else:
            messages.error(request, str(request.POST.get('school')) + ' Failed to be Updated')
        return HttpResponseRedirect("/manager/schools/")
    else:
        schoolObj = School.objects.get(id=schoolId)
        context = ''
        context += '<form action="/manager/editSchool/'+str(schoolObj.id)+'/" method="POST" id="">'

        context += '<div class="form-group">'
        context += '<label>School Name</label>'
        context += '<input type="text" name="school" value="'+str(schoolObj.name)+'" class="form-control" required />'
        context += '</div>'

        context += '<div class="form-group">'
        context += '<label>School Code</label>'
        context += '<input type="text" name="code" value="'+str(schoolObj.code)+'" class="form-control" required />'
        context += '</div>'

        context += '<div class="form-group">'
        context += '<center>'
        context += '<button type="submit" class="btn btn-success btn-lg">'
        context += 'UPDATE'
        context += '</button>'
        context += '</center>'
        context += '</div>'
        context += '</form>'
    return HttpResponse(context)

@login_required
@csrf_exempt
def groups(request):
    if request.method == 'POST':
        newGroup = Group()
        newGroup.name = request.POST.get('group')
        if Group.objects.filter(name=request.POST.get('group')).count() == 0:
            newGroup.save()
            if Group.objects.filter(name=request.POST.get('group')).count() > 0:
                messages.success(request, request.POST.get('group') + ' Successfully Registered')
            else:
                messages.error(request, "Failed to Register " + request.POST.get('group'))
        else:
            pass
        return HttpResponseRedirect("/manager/groups/")
    if request.method == 'GET' and 'key' in request.GET:
        key = request.GET.get('key')
        groups = Group.objects.filter(name__icontains=key).order_by('name')
    else:
        groups = Group.objects.all().order_by('name')
    context = {
        "groups": groups,
        "title": 'Groups',
    }
    return render(request, "manager/groups.html", context)


@login_required
def deleteGroup(request, groupId):
    groupObj = Group.objects.get(id=groupId)
    groupName = groupObj.name
    groupObj.delete()
    if Group.objects.filter(id=groupId).count() == 0:
        messages.success(request, groupName + " Successfully Deleted")
    else:
        messages.error(request, "Failed to Delete " + groupName)
    return HttpResponseRedirect("/manager/groups/")


@login_required
@csrf_exempt
def schoolCourses(request, schoolId):
    if request.method == 'POST':
        newCourse = Courses()
        newCourse.school_id = schoolId
        newCourse.name = request.POST.get('course')
        newCourse.code = request.POST.get('code')
        newCourse.level_id = request.POST.get('level')
        newCourse.course_category_id = request.POST.get('category')
        if Courses.objects.filter(name=request.POST.get('course'), code=request.POST.get('code'), school_id=schoolId).count() == 0:
            newCourse.save()
        else:
            pass
        return HttpResponseRedirect("/manager/schoolCourses/"+str(schoolId)+"/")
    if request.method == 'GET' and 'key' in request.GET:
        key = request.GET.get('key')
        courses = Courses.objects.filter(school_id=schoolId).filter(Q(name__icontains=key) | Q(code__icontains=key)).order_by('-name')
    else:
        courses = Courses.objects.filter(school_id=schoolId).order_by('-name')
    context = {
        "courses": courses,
        "schoolId": schoolId,
        "categories": CourseCategory.objects.all().exclude(is_active=False),
        "levels": CourseLevel.objects.all().exclude(is_active=False),
        "title": 'Courses',
    }
    return render(request, "manager/courses.html", context)


@login_required
@csrf_exempt
def courseSubjects(request, courseId):
    courseObj = Courses.objects.get(id=courseId)
    if request.method == 'POST':
        newSubject = Subjects()
        newSubject.course_id = courseId
        newSubject.name = request.POST.get('subject')
        newSubject.code = request.POST.get('code')
        newSubject.year_id = request.POST.get('year')
        newSubject.academic_id = request.POST.get('academic')
        yearObj = Year.objects.get(code=request.POST.get('year'))
        if Subjects.objects.filter(name=request.POST.get('subject'), code=request.POST.get('code'),
                                   year_id=yearObj.id, course_id=courseId).count() == 0:
            newSubject.save()
        else:
            pass
        return HttpResponseRedirect("/manager/courseSubjects/"+courseId+"/")
    if request.method == 'GET' and 'key' in request.GET:
        key = request.GET.get('key')
        subjects = Subjects.objects.filter(course_id=courseId).filter(Q(name__icontains=key) | Q(code__icontains=key)).order_by('-name')
    else:
        subjects = Subjects.objects.filter(course_id=courseId).order_by('-name')
    context = {
        "courseId": courseId,
        "schoolId": courseObj.school_id,
        "subjects": subjects,
        "years": Year.objects.all(),
        "academics": AcademicYear.objects.all().exclude(is_active=False),
        "title": 'Subjects',
    }
    return render(request, "manager/subjects.html", context)


@login_required
def deleteCourse(request, courseId):
    courseObj = Courses.objects.get(id=courseId)
    schoolId = courseObj.school_id
    course_name = courseObj.name
    if Courses.objects.filter(id=courseId).count() == 0:
        messages.success(request, str(course_name)+' Successfully Deleted')
    else:
        messages.error(request, str(course_name)+' Failed To Delete, Please Try again')
    courseObj.delete()
    return HttpResponseRedirect("/manager/schoolCourses/"+str(schoolId)+"/")


@login_required
def deleteCourseSubjects(request, subjectId):
    subjectObj = Subjects.objects.get(id=subjectId)
    courseId = subjectObj.course_id
    subject_name = subjectObj.name
    subjectObj.delete()
    if Subjects.objects.filter(id=subjectId).count() == 0:
        messages.success(request, str(subject_name)+' Successfully Deleted')
    else:
        messages.error(request, str(subject_name)+' Failed to Deleted, Please Try again')
    return HttpResponseRedirect("/manager/courseSubjects/"+str(courseId)+"/")



@login_required
def courseSubjectsActivator(request, key, subjectId):
    subjectObj = Subjects.objects.get(id=subjectId)
    if key == 'activate':
        subjectObj.is_active = True
        subjectObj.save()

        activateSubject = Subjects.objects.get(id=subjectId)
        if activateSubject.is_active:
            messages.success(request, str(activateSubject.name)+' Successfully Activated')
        else:
            messages.error(request, str(activateSubject.name)+' Failed to Activate, Please Try again')
    elif key == 'deactivate':
        subjectObj.is_active = False
        subjectObj.save()

        deactivatedSubject = Subjects.objects.get(id=subjectId)
        if deactivatedSubject.is_active:
            messages.error(request, str(deactivatedSubject.name)+' Failed to Deactivated Please Try again')
        else:
            messages.success(request, str(deactivatedSubject.name)+ ' Successfully Deactivated')

    return HttpResponseRedirect("/manager/courseSubjects/"+str(subjectObj.course_id)+"/")


@login_required
def courseActivator(request, key, courseId):
    courseObj = Courses.objects.get(id=courseId)
    if key == 'activate':
        courseObj.is_active = True
        courseObj.save()

        activatedCourse = Courses.objects.get(id=courseId)
        if activatedCourse.is_active:
            messages.success(request, str(activatedCourse.name) + ' Successfully Activated')
        else:
            messages.error(request, str(activatedCourse.name) + ' Failed to Activate, Please Try again')
    elif key == 'deactivate':
        courseObj.is_active = False
        courseObj.save()

        deactivatedCourse = Courses.objects.get(id=courseId)
        if deactivatedCourse.is_active:
            messages.error(request, str(deactivatedCourse.name) + ' Failed to Deactivate, please Try again')
        else:
            messages.success(request, str(deactivatedCourse.name) + ' Successfully Deactivated')

    return HttpResponseRedirect("/manager/schoolCourses/"+str(courseObj.school_id)+"/")


@login_required
def feedbacks(request, key):
    if key == 'all':
        feedBacks = Feedback.objects.all()
        title = 'Feedbaks'
        total = Feedback.objects.all().count()
    elif key == 'ratings':
        feedBacks = Feedback.objects.all().exclude(satisfaction='').exclude(satisfaction=None).order_by('-updated')
        title = 'Satisfactions & Ratings'
        total = Feedback.objects.all().exclude(satisfaction='').exclude(satisfaction=None).count()
    elif key == 'oldfeatures':
        feedBacks = Feedback.objects.all().exclude(features='').exclude(features=None).order_by('-updated')
        title = 'Old Features'
        total = Feedback.objects.all().exclude(features='').exclude(features=None).count()
    elif key == 'newfeatures':
        feedBacks = Feedback.objects.all().exclude(addfeatures='',).exclude(addfeatures=None).order_by('-updated')
        title = 'New Features'
        total = Feedback.objects.all().exclude(addfeatures='',).exclude(addfeatures=None).count()
    elif key == 'problems':
        feedBacks = Feedback.objects.all().exclude(problems='').exclude(problems=None).order_by('-updated')
        title = 'Problems'
        total = Feedback.objects.all().exclude(problems='').exclude(problems=None).count()
    else:
        feedbacks = ''
        title = 'Feedbacks'
    context = {
        "feedbaks": feedBacks,
        "title": title,
        "key": key,
        "total": total,
    }
    return render(request, "manager/feedbacks.html", context)



@csrf_exempt
def editSubject(request, subjectId):
    if request.method == 'POST':
        if Subjects.objects.filter(id=subjectId).count() > 0:
            subjectObject = Subjects.objects.get(id=subjectId)
            subjectObject.name = request.POST.get('subject')
            subjectObject.code = request.POST.get('code')
            subjectObject.year_id = request.POST.get('year')
            subjectObject.academic_id = request.POST.get('academic')
            subjectObject.save()

            newUpdatedSubject = Subjects.objects.get(id=subjectId)
            messages.success(request, str(newUpdatedSubject.name) + ' Successfully Updated')
            return HttpResponseRedirect("/manager/courseSubjects/" +str(newUpdatedSubject.course.id)+"/")
    else:
        subjectObj = Subjects.objects.get(id=subjectId)
        context = ''
        context += '<form role="form" action="/manager/editSubject/'+str(subjectId)+'/" ' \
                   'method="POST" id="editSubjectForm">'
        context += '<div class="form-group">'
        # context += '<input type="text" name="course" class="form-control hidden" ' \
        #            'id="course" value="'++'" required />'
        # context += '</div>'
        context += '<div class="form-group">'
        context += '<label>Subject Name</label>'
        context += '<input type="text" name="subject" class="form-control" value="'+str(subjectObj.name)+'" required />'
        context += '</div>'
        context += '<div class="form-group">'
        context += '<label>Subject Code</label>'
        context += '<input type="text" name="code" class="form-control" value="'+str(subjectObj.code)+'" required />'
        context += '</div>'
        context += '<div class="form-group">'
        context += '<label>Year</label>'
        context += '<select name="year" class="form-control" required>'
        if subjectObj.year_id != None:
            context += '<option value="'+str(subjectObj.year_id)+'">'+str(subjectObj.year.name)+'('+str(subjectObj.year.code)+')</option>'
        else:
            context += '<option value="">Please Select ...</option>'
        yearsObj = Year.objects.all().exclude(id=subjectObj.year.id)
        for year in yearsObj:
            context += '<option value="'+str(year.id)+'">'+str(year.name)+'('+str(year.code)+')</option>'
        context += '</select>'
        context += '</div>'

        context += '<div class="form-group">'
        context += '<label>Academic Year</label>'
        context += '<select name="academic" class="form-control" required >'
        if subjectObj.academic_id != None:
            context += '<option value="'+str(subjectObj.academic_id)+'">'+str(subjectObj.academic.name)+'</option>'
        else:
            context += '<option value="">Please Select ...<option>'
        academicYearsObj = AcademicYear.objects.all().exclude(id=subjectObj.academic_id)
        for academicYear in academicYearsObj:
            context += '<option value="'+str(academicYear.id)+'">'+str(academicYear.name)+'</option>'
        context += '</select>'
        context += '</div>'
        context += '<div class="form-group">'
        context += '<center>'
        context += '<button type="submit" class="btn btn-success btn-lg">ADD</button>'
        context += '</center>'
        context += '</div>'
        context += '</form>'
        return HttpResponse(context)



@login_required
@csrf_exempt
def searchRelatedSubject(request):
    context = ''
    if request.method == 'POST':
        key = request.POST.get('search')
        context += '<table class="table table-striped">'
        subjects = Subjects.objects.filter(Q(name__icontains=key) | Q(code__icontains=key))
        if Subjects.objects.filter(Q(name__icontains=key) | Q(code__icontains=key)).count() > 0:
            for subject in subjects:
                context += '<tr>'
                context += '<td>'+subject.name+'</td>'
                context += '<td>'+subject.code+'</td>'
                context += '<td><a href="javascript:;" ' \
                           'onclick="loadSubjectForm('+str(subject.id)+');" data-toggle="tooltip" ' \
                           'data-placement="top" title="Use this Subject"><i class="fa fa-plus"></i></a></td>'
                context += '</tr>'
        else:
            context += '<div class="alert alert-warning"><center>No Related Subject(s)</center></div>'
        context += '</table>'
    return HttpResponse(context)

@login_required
def loadRelatedSubjectContent(request, subjectId):
    context = ''
    subjectObj = Subjects.objects.get(id=subjectId)
    context += '<div class="form-group">'
    context += '<label>Subject Name</label>'
    context += '<input type="text" class="form-control" name="subject" value="'+str(subjectObj.name)+'" required />'
    context += '</div>'

    context += '<div class="form-group">'
    context += '<label>Subject Code</label>'
    context += '<input type="text" class="form-control" name="code" value="'+str(subjectObj.code)+'" required />'
    context += '</div>'
    return HttpResponse(context)
