#################################################################################
# Author: Daniel Peter Kindimba
# Project: ScholarNet
#################################################################################
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpRequest, Http404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import *
from django.core import serializers
from app.views import *
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
import json
import logging


def set_access_control_headers(response):
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Credentials'] = 'false'
    response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response['Access-Control-Max-Age'] = 1000
    response['Access-Control-Allow-Headers'] = '*'

class HttpOptionsDecorator(object):
    def __init__(self, f):
        self.f = f

    def __call__(self, *args):
        logging.info("Call decorator")
        request = args[0]
        if request.method == "OPTIONS":
            response = HttpResponse()
            set_access_control_headers(response)
            return response
        else:
            response = self.f(*args)
            set_access_control_headers(response)
            return response



###########################################################################################
# function to mobile users to login
###########################################################################################
# @login_required
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



############################################################################################
#function returning the list of subjects post content
############################################################################################
@never_cache
def postList(request):
    if request.GET.get('offset') != '':
        offset = 0
    else:
        offset = request.GET.get('offset')
    initialOffset = 15
    posts = Descriptions.objects.all().values().order_by('-updated')[offset:initialOffset+offset]
    total = Descriptions.objects.all().count()
    context = ''
    content = []
    for post in posts:
        postObj = Descriptions.objects.get(id=post['id'])
        images = Images.objects.filter(description_id=post['id']).count()
        user = User.objects.get(id=post['user_id'])
        for gp in user.groups.all():
            group = gp
        info = {}
        info = {
            'id': post['id'],
            'display': user.profile.display,
            'role': str(group),
            'description': post['description'][:600],
            'updated': str(post['updated'].strftime("%d/%m/%Y   @  %I:%M %p")),
            'recommendation': postObj.recommend,
            'comments': postObj.comments,
            'images': images,
            'user': str(postObj.user.username),
        }
        content.append(info)

    return HttpResponse(json.dumps(content))





############################################################################################
#function returning the list of subjects post content
############################################################################################
@never_cache
def postSubjectList(request):
    subjectId = request.GET.get('id')
    posts = Descriptions.objects.filter(subject_id=subjectId).values().order_by('-updated')[:100]
    total = Descriptions.objects.filter(subject_id=subjectId).count()
    context = ''
    content = []
    for post in posts:
        postObj = Descriptions.objects.get(id=post['id'])
        images = Images.objects.filter(description_id=post['id']).count()
        user = User.objects.get(id=post['user_id'])
        for gp in user.groups.all():
            group = gp
        info = {}
        info = {
            'id': post['id'],
            'display': user.profile.display,
            'role': str(group),
            'description': post['description'],
            'updated': str(post['updated'].strftime("%d/%m/%Y   @  %I:%M %p")),
            'recommendation': postObj.recommend,
            'comments': postObj.comments,
            'images': images,
            'user': str(postObj.user.username),
        }
        content.append(info)

    return HttpResponse(json.dumps(content))