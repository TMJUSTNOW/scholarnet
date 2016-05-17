#################################################################################
# Author: Daniel Peter Kindimba
# Project: ScholarNet
#################################################################################
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpRequest, Http404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from functools import wraps
from django.middleware.csrf import CsrfViewMiddleware, get_token
from django.utils.decorators import available_attrs, decorator_from_middleware
from django.views.decorators.clickjacking import xframe_options_deny
from django.contrib.auth.models import *
from django.core import serializers
from app.views import *
from django.contrib import auth
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.contrib.humanize.templatetags import humanize
from functools import wraps
import json

###########################################################################################
# function to mobile users to login
###########################################################################################
def login(request):
    if request.method == 'GET':
        username = internationalizePhone(request.GET.get('username'))
        password = request.GET.get('password')

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                data = User.objects.get(id=request.user.id)
                response = data.profile.course_id
                return HttpResponse(str(response))
            else:
                return HttpResponse('0')
        else:
            response = '0'
            return HttpResponse(response)
    else:
        return HttpResponse('0')


#######################################################################################
# function returnign institue as a json
######################################################################################
@never_cache
def instituteList(request):
    institutes = School.objects.values('id','name','code')
    response = json.dumps([i for i in institutes])

    return HttpResponse(response)



######################################################################################
#function for returning the institute Course List
#######################################################################################
@never_cache
def courseList(request):
    school_data = request.GET.get('college')
    courses = Courses.objects.filter(school_id=school_data).values('id','name','code')
    response = json.dumps([i for i in courses])
    return HttpResponse(response)


#########################################################################################
#   function returning list of Subjects for a particular User
########################################################################################
@never_cache
def userSubjectList(request):
    if request.method == 'GET':
        course = request.GET.get('course')
        user = internationalizePhone(request.GET.get('user'))
        #getting the user year_id
        userObj = User.objects.get(username=user)

        if course != None:
            subjects = Subjects.objects.filter(course_id=int(course),
                                               year_id=userObj.profile.year_id).values('id', 'name', 'code')
        else:
            subjects = ''
        response = json.dumps([i for i in subjects])

    return HttpResponse(response)



############################################################################################
#function returning the list of subjects post content
############################################################################################
@never_cache
def postSubjectListAll(request):
    subjects = ''
    content = []
    if request.method == 'GET' and 'phone' in request.GET and 'offset' in request.GET:
        userPhone = internationalizePhone(request.GET.get('phone'))
        if User.objects.filter(username=userPhone).exists():
            cUser = User.objects.get(username=userPhone)
            for ugroup in cUser.groups.all():
                if ugroup.name == 'Teacher':
                    subjects_ids = []
                    teacherSubjects = TeacherSubject.objects.filter(user_id=cUser.id)
                    for tsubject in teacherSubjects:
                        subjects_ids.append(tsubject.subject.id)
                    subjects = Subjects.objects.filter(id__in=subjects_ids)
                elif ugroup.name == 'Student':
                    subjects = Subjects.objects.filter(course_id=cUser.profile.course.id)

            subject_ids = []

            for sub in subjects:
                subject_ids.append(sub.id)

            offset_limit=5
            if int(request.GET.get('offset')) == 0:
                offset = 0
            else:
                offset = int(request.GET.get('offset'))-1
            posts = Descriptions.objects.filter(subject_id__in=subject_ids).values().order_by('-updated')[int(offset)*offset_limit:(int(offset)*offset_limit)+offset_limit]
            total = Descriptions.objects.filter(subject_id__in=subject_ids).count()
            for post in posts:
                postObj = Descriptions.objects.get(id=post['id'])
                images = Images.objects.filter(description_id=post['id']).count()
                user = User.objects.get(id=post['user_id'])
                for gp in user.groups.all():
                    group = gp
                info = {}
                updated = ''
                if humanize.naturalday(post['updated']) == 'today':
                    updated = humanize.naturaltime(post['updated'])
                else:
                    updated = humanize.naturalday(post['updated'])
                info = {
                    'id': post['id'],
                    'display': user.profile.display,
                    'role': str(group),
                    'description': post['description'],
                    'updated': updated,
                    'recommendation': postObj.recommend,
                    'comments': postObj.comments,
                    'images': images,
                    'user': str(postObj.user.username),
                }
                content.append(info)
        else:
            pass
    else:
        pass

    return HttpResponse(json.dumps(content))




############################################################################################
#function returning the list of subjects post content
############################################################################################
@never_cache
def postSubjectList(request):
    subjectId = request.GET.get('id')
    offset_limit=5
    if int(request.GET.get('offset')) == 0:
        offset = 0
    else:
        offset = int(request.GET.get('offset'))-1
    posts = Descriptions.objects.filter(subject_id=subjectId).values().order_by('-updated')[int(offset)*offset_limit:(int(offset)*offset_limit)+offset_limit]
    total = Descriptions.objects.filter(subject_id=subjectId).count()
    content = []
    for post in posts:
        postObj = Descriptions.objects.get(id=post['id'])
        images = Images.objects.filter(description_id=post['id']).count()
        user = User.objects.get(id=post['user_id'])
        for gp in user.groups.all():
            group = gp
        info = {}
        updated = ''
        if humanize.naturalday(post['updated']) == 'today':
            updated = humanize.naturaltime(post['updated'])
        else:
            updated = humanize.naturalday(post['updated'])
        info = {
            'id': post['id'],
            'display': user.profile.display,
            'role': str(group),
            'description': post['description'],
            'updated': updated,
            'recommendation': postObj.recommend,
            'comments': postObj.comments,
            'images': images,
            'user': str(postObj.user.username),
        }
        content.append(info)

    return HttpResponse(json.dumps(content))


###########################################################################################
# fucntion for getting all the post comments
###########################################################################################
@never_cache
def getPostComments(request):
    postId = request.GET.get('post')
    # offset_limit = 5
    # if int(request.GET.get('offset')) == 0:
    #     offset = 0
    # else:
    #     offset = int(request.GET.get('offset')) - 1
    # comments = DescriptionsComments.objects.filter(description_id=postId).order_by('-updated')[int(offset)*offset_limit:(int(offset)*offset_limit)+offset_limit]
    comments = DescriptionsComments.objects.filter(description_id=postId).order_by('-updated')
    content = []
    for comment in comments:
        info = {}
        userObj = User.objects.get(id=comment.user_id)
        updated = ''
        if humanize.naturalday(comment.updated) == 'today':
            updated = humanize.naturaltime(comment.updated)
        else:
            updated = humanize.naturalday(comment.updated)
        info = {
            'id': comment.id,
            'info': comment.comment,
            'poster': userObj.profile.display,
            'date': updated,
        }
        content.append(info)
    return HttpResponse(json.dumps(content))

###############################################################################################
# function for setting the Post Comment
###############################################################################################
def setPostComment(request):
    postId = request.GET.get('post')
    user = internationalizePhone(request.GET.get('user'))
    comment = request.GET.get('comment')

    #getting the user_id
    userObj = User.objects.get(username=user)
    #Initializing the comment object
    newComment = DescriptionsComments()
    newComment.user_id = userObj.id
    newComment.comment = comment
    newComment.description_id = postId
    newComment.save()
    if DescriptionsComments.objects.filter(description_id=postId, user_id=userObj.id, comment=comment).count() > 0:
        response = '1'
    else:
        response = '0'
    return HttpResponse(response)


#################################################################################################################
# fucntion for getting all the post images
#################################################################################################################
@never_cache
def getPostImages(request):
    postId = request.GET.get('post')
    images = Images.objects.filter(description_id=postId)
    content = []
    for image in images:
        info = {}
        info = {
            "id": image.id,
            "image": 'static/'+str(image.url),
        }
        content.append(info)
    return HttpResponse(json.dumps(content))



###################################################################################################################
# function for getting the Display Name of the user
###################################################################################################################
@never_cache
def getDisplayName(request):
    user = internationalizePhone(request.GET.get('user'))
    userObj = User.objects.get(username=user)
    content = []
    info = {
        'display': userObj.profile.display,
        'courseId': int(userObj.profile.course_id),
        'year': int(userObj.profile.year.code),
    }
    content.append(info)
    return HttpResponse(json.dumps(content))




####################################################################################################################
# function for registering a post
####################################################################################################################
@xframe_options_deny
@csrf_exempt
def setPost(request):
    if request.method == 'POST':
        user = internationalizePhone(request.POST.get('user'))
        subject = request.POST.get('subject')
        article = request.POST.get('article')

        #getting the userId
        userObj = User.objects.get(username=user)
        new_post = Descriptions()
        new_post.user_id = userObj.id
        new_post.description = article
        new_post.subject_id = subject
        if Descriptions.objects.filter(user_id=userObj.id, description=article, subject_id=subject).count() == 0:
            new_post.save()

        savedArticle = Descriptions.objects.filter(user_id=userObj.id, description=article, subject_id=subject)
        for article in savedArticle:
            articleObj = article

        for filename, file in request.FILES.items():
            newImage = Images()
            newImage.description_id=articleObj.id
            newImage.url = request.FILES[filename]
            if Images.objects.filter(description_id=articleObj.id, name=request.FILES[filename].name).count() == 0:
                newImage.save()
        response = HttpResponse(json.dumps({"message": "Successfully Post"}))
    else:
        response = HttpResponse(json.dumps({"message": "Failed Post"}))

    return HttpResponse(response)


def deletePost(request):
    post = request.GET.get('post')
    if Descriptions.objects.filter(id=post).count() > 0:
        postObj = Descriptions.objects.get(id=post)
        postCommentObj = DescriptionsComments.objects.filter(description_id=post)
        postImagesObj = Images.objects.filter(description_id=post)
        postLikesObj = Likes.objects.filter(description_id=post)

        postObj.delete()
        for postCommentO in postCommentObj:
             postCommentO.delete()
        for postImagesO in postImagesObj:
            postImagesO.delete()
        for postLikesO in postLikesObj:
            postLikesO.delete()
        response = '1'
    else:
        response = '0'
    return HttpResponse(response)

def updatePost(request):
    response = '1'
    content = request.GET.get('article')
    postId = request.GET.get('articleId')

    articleObj = Descriptions.objects.get(id=postId)
    articleObj.description = content
    articleObj.save()
    return HttpResponse(response)




#####################################################################################################################
# function for uploading images
#####################################################################################################################
@csrf_exempt
def setImage(request):
    response = ''
    iamge = request.FILES['image']
    return HttpResponse(response)


#####################################################################################################################
# function for getting total number of comments given PostId
#####################################################################################################################
@never_cache
def getTotalComRecCount(request):
    postId = request.GET.get('post')
    postObj = Descriptions.objects.get(id=postId)
    response = [
        {
            'comments': postObj.comments,
            'recommendations': postObj.recommend,
        }
    ]
    return HttpResponse(json.dumps(response))



######################################################################################################################
# Function for recommending on a post
######################################################################################################################
def setRecommendation(request):
    postId = request.GET.get('post')
    user = internationalizePhone(request.GET.get('user'))
    userObj = User.objects.get(username=user)
    if Likes.objects.filter(user_id=userObj.id, description_id=postId).count() > 0:
        likeObj = Likes.objects.get(Q(user_id=userObj.id) & Q(description_id=postId))
        likeObj.delete()
    else:
        likeObj = Likes()
        likeObj.user_id = userObj.id
        likeObj.description_id = postId
        likeObj.save()
    response = ''
    return HttpResponse(response)






#############################################################################################
# A function returning the User lsit As a Json
############################################################################################
@never_cache
def usersList(request):
    response = json.dumps([i for i in User.objects.values('id','username')])
    return HttpResponse(response)





#############################################################################################
# A fucntion for Resseting the User password
#############################################################################################
def passwordResset(request):
    if User.objects.filter(username=internationalizePhone(request.GET.get('phone'))).count() > 0:
        phone = internationalizePhone(request.GET.get('phone'))
        password = request.GET.get('password')
        user = User.objects.get(username=phone)
        user.set_password(password)
        user.save()
        response = 1
    else:
        response = 0
    return HttpResponse(response)


##############################################################################################
# A fucntion for Mobile User Registration Using the GET method
##############################################################################################
def register(request):
    if request.method == 'GET':
        if request.GET.get('username') != None:
            username = internationalizePhone(request.GET.get('phone'))
            password = request.GET.get('password')
            institute = request.GET.get('college')
            role = request.GET.get('role')
            course = request.GET.get('course')
            year = request.GET.get('year')
            display = request.GET.get('username')

            #getting the year_id
            yearObj = Year.objects.get(code=year)


            if User.objects.filter(username=username).exists():
                response = 'User already exists'
                return HttpResponse(response)
            else:
                user = User()
                user.username = username
                user.set_password(password)
                user.is_active = True
                user.save()

                #creating the user profile
                newUser = User.objects.get(username=username)

                #assining a group of the registered user
                if role.lower() == 'educator':
                    groupname = 'Educator'
                elif role.lower() == 'student':
                    groupname = 'Student'
                group = Group.objects.get(name=groupname)
                newUser.groups.add(group)

                userp = UserProfile()
                userp.user_id = newUser.id
                userp.school_id = institute
                userp.course_id = course
                userp.year_id = yearObj.id
                userp.display = display
                userp.save()
                if User.objects.filter(username=username).exists() and UserProfile.objects.filter(user=User.objects.get(username=username)).exists():
                    response = '1'
                else:
                    response = '0'
                return HttpResponse(response)
        else:
            return HttpResponse("Bad Request")
    else:
        return HttpResponse('Bad Request')



####################################################################################################
# A function for returning a list of of recovery confirmation
####################################################################################################
@never_cache
def getRequestConfirmationList(request):
    content = []
    info = {}
    requestList = Recovery.objects.filter(waiting=False)[:10]
    if Recovery.objects.filter(waiting=False).count() > 0:
        for rl in requestList:
            sentRequest = Recovery.objects.get(id=rl.id)
            sentRequest.waiting = True
            sentRequest.save()
            info = {}
            info = {
                'id': rl.id,
                'phone': rl.phone,
                'code': rl.code,
            }
            content.append(info)
    return HttpResponse(json.dumps(content))


####################################################################################################
# A function for managing user reported problems
####################################################################################################
def reportProblem(request):
    user = request.GET.get('user')
    problem = request.GET.get('problem')

    newProblem = Feedback()
    userObj = User.objects.get(username=internationalizePhone(user))
    newProblem.user_id = userObj.id
    newProblem.problems = problem
    newProblem.save()

    response = 1
    return HttpResponse(response)



def setYear(request):
    user = request.GET.get('phone')
    year = request.GET.get('year')
    yearObj = Year.objects.get(code=year)
    userObj = User.objects.get(username=internationalizePhone(user))
    userProfObj = UserProfile.objects.get(user_id=userObj.id)
    userProfObj.year_id = yearObj.id
    userProfObj.save()
    response = 1
    return HttpResponse(response)





######################################################################################################
#A function  for Changing the display name
######################################################################################################
def setDisplayName(request):
    phone = internationalizePhone(request.GET.get('phone'))
    display = request.GET.get('display')
    user = User.objects.get(username=phone)
    userProfile = UserProfile.objects.get(user_id=user.id)
    userProfile.display = display
    userProfile.save()
    response = '1'
    return HttpResponse(response)




"""
A function for Getting the Sdrive file according to the subjects
"""
def sdrive(request):
    subject = request.GET.get('subject')
    sdriveObjects = Sdrive.objects.filter(subject_id=subject)
    content = []
    for sdo in sdriveObjects:
        info = {}
        info = {
            "date": str(sdo.updated),
            "url": str(sdo.file),
            "extension": '',
            "caption": sdo.title,
        }
        content.append(info)

    return HttpResponse(json.dumps(content))


"""
A function for Uploading the Sderive Files to the system
"""
@csrf_exempt
def sdriveUploader(request):
    if request.method == 'POST':
        if request.POST or None:
            newSdriveObject = Sdrive()
            newSdriveObject.subject_id = request.POST.get('subject')
            newSdriveObject.title = request.POST.get('title')
            newSdriveObject.file = request.FILES['title']
            content = []
            try:
                newSdriveObject.save()
                info = {}
                info = {
                    "status": True,
                    "message": "File Successfully Uploaded"
                }
                content.append(info)
            except:
                info = {}
                info = {
                    "status": False,
                    "message": "Failed to Upload File"
                }
                content.append(info)
            return HttpResponse(json.dumps(content))
        else:
            content = []
            info = {}
            info = {
                "status": False,
                "message": "Failed to Upload File"
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






