from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpRequest, Http404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from endless_pagination.decorators import page_template
from django.template import RequestContext
from django.contrib.auth.models import *
from django.views.decorators.csrf import csrf_exempt
from app.models import *

@login_required
def home(request):
    context = {
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
    context = {
        "memberName": 'Adminstrators',
        "activatorSwitcher": 'adminstratorsActivator',
        "memberType": 'adminstrator',
        "members": User.objects.filter(is_superuser=True),
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
    elif key == 'deactivate':
        adminstratorObj.is_active = False
        adminstratorObj.save()
    return HttpResponseRedirect("/manager/adminstrators/")


@login_required
@page_template('manager/common/paginated_members.html')
def students(request, template='manager/members.html', extra_context=None):
    context = {
        "memberName": 'Students',
        "activatorSwitcher": 'studentsActivator',
        "memberType": 'student',
        "members": User.objects.filter(groups__name='Student'),
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
    elif key == 'deactivate':
        studentObj.is_active = False
        studentObj.save()
    return HttpResponseRedirect("/manager/students/")


@login_required
@page_template('manager/common/paginated_members.html')
def educators(request, template='manager/members.html', extra_context=None):
    context = {
        "memberName": 'Educators',
        "activatorSwitcher": 'educatorsActivator',
        "memberType": 'educator',
        "members": User.objects.filter(groups__name='Educator'),
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
    elif key == 'deactivate':
        educatorObj.is_active = False
        educatorObj.save()
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
            return HttpResponseRedirect("/manager/schools/")
        else:
            return HttpResponseRedirect("/manager/schools/")
    context = {
        "schools": School.objects.all(),
        "title": 'Schools',
    }
    return render(request, "manager/schools.html", context)


@login_required
def schoolsActivator(request, key, schoolId):
    schoolObj = School.objects.get(id=schoolId)
    if key == 'activate':
        schoolObj.is_active = True
        schoolObj.save()
    elif key == 'deactivate':
        schoolObj.is_active = False
        schoolObj.save()
    return HttpResponseRedirect("/manager/schools/")


@login_required
@csrf_exempt
def groups(request):
    if request.method == 'POST':
        newGroup = Group()
        newGroup.name = request.POST.get('group')
        if Group.objects.filter(name=request.POST.get('group')).count() == 0:
            newGroup.save()
        else:
            pass
        return HttpResponseRedirect("/manager/groups/")
    context = {
        "groups": Group.objects.all(),
        "title": 'Groups',
    }
    return render(request, "manager/groups.html", context)


@login_required
def deleteGroup(request, groupId):
    groupObj = Group.objects.get(id=groupId)
    groupObj.delete()
    return HttpResponseRedirect("/manager/groups/")


@login_required
@csrf_exempt
def schoolCourses(request, schoolId):
    if request.method == 'POST':
        newCourse = Courses()
        newCourse.school_id = schoolId
        newCourse.name = request.POST.get('course')
        newCourse.code = request.POST.get('code')
        newCourse.course_category_id = request.POST.get('category')
        if Courses.objects.filter(name=request.POST.get('course'), code=request.POST.get('code'), school_id=schoolId).count() == 0:
            newCourse.save()
        else:
            pass
        return HttpResponseRedirect("/manager/schoolCourses/"+str(schoolId)+"/")
    context = {
        "courses": Courses.objects.filter(school_id=schoolId).order_by('-name'),
        "schoolId": schoolId,
        "categories": CourseCategory.objects.all().exclude(is_active=False),
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
        yearObj = Year.objects.get(code=request.POST.get('year'))
        if Subjects.objects.filter(name=request.POST.get('subject'), code=request.POST.get('code'), year_id=yearObj.id).count() == 0:
            newSubject.save()
        else:
            pass
        return HttpResponseRedirect("/manager/courseSubjects/"+courseId+"/")
    context = {
        "courseId": courseId,
        "schoolId": courseObj.school_id,
        "subjects": Subjects.objects.filter(course_id=courseId).order_by('-name'),
        "title": 'Subjects',
    }
    return render(request, "manager/subjects.html", context)


@login_required
def deleteCourse(request, courseId):
    courseObj = Courses.objects.get(id=courseId)
    schoolId = courseObj.school_id
    courseObj.delete()
    return HttpResponseRedirect("/manager/schoolCourses/"+str(schoolId)+"/")


@login_required
def deleteCourseSubjects(request, subjectId):
    subjectObj = Subjects.objects.get(id=subjectId)
    courseId = subjectObj.course_id
    subjectObj.delete()
    return HttpResponseRedirect("/manager/courseSubjects/"+str(courseId)+"/")



@login_required
def courseSubjectsActivator(request, key, subjectId):
    subjectObj = Subjects.objects.get(id=subjectId)
    if key == 'activate':
        subjectObj.is_active = True
        subjectObj.save()
    elif key == 'deactivate':
        subjectObj.is_active = False
        subjectObj.save()

    return HttpResponseRedirect("/manager/courseSubjects/"+str(subjectObj.course_id)+"/")


@login_required
def courseActivator(request, key, courseId):
    courseObj = Courses.objects.get(id=courseId)
    if key == 'activate':
        courseObj.is_active = True
        courseObj.save()
    elif key == 'deactivate':
        courseObj.is_active = False
        courseObj.save()

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
