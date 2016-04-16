from django.conf.urls import patterns, include, url
from tastypie.authorization import Authorization
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.utils import trailing_slash
from django.contrib.auth import authenticate, login, logout
from tastypie.http import HttpUnauthorized, HttpForbidden, HttpNotFound
from django.http import HttpRequest, Http404, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth.models import *
from app.models import *


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        allowed_methods = ['get', 'post', 'put']
        resource_name = 'user'
        fields = ['id', 'first_name', 'last_name', 'username', 'is_active']
        authorization = Authorization()
        filtering = {
            'id': ALL,
            'username': ALL,
        }

    def prepend_urls(self):
        return [
            url(r"^user/login/$", self.wrap_view('login'), name="api_login"),
            url(r"^user/logout/$", self.wrap_view('logout'), name='api_logout'),
            url(r"^user/register/$", self.wrap_view('register'), name='api_register'),
        ]

    """
    This function will perform the task of Registering, Activating the Validation Process
    """
    def register(self, request, **kwargs):
        self.method_check(request, allowed=['post'])

        data = self.deserialize(request, request.body,
                                format=request.META.get('CONTENT_TYPE', 'application/json'))
        username = data.get('username', '')
        password = data.get('password', '')
        display = data.get('display', '')
        role = data.get('role', '')

        newUser = User()
        newUser.username = username
        newUser.set_password(password)
        newUser.is_active = False
        newUser.save()

        #Creating the Default user Profile
        if User.objects.filter(username=username).exists():
            newUserObject = User.objects.get(username=username)
            newUserProfile = UserProfile()
            newUserProfile.user_id = newUserObject.id
            newUserProfile.display = display
            newUserProfile.save()

        #Registering the user role
        if User.objects.filter(username=username).exists():
            if role.lower() == 'educator':
                groupname = 'Educator'
            elif role.lower() == 'student':
                groupname = 'Student'
            group = Group.objects.get(name=groupname)
            newUserObject.groups.add(group)

        #Checking if the User is successfully Registered or Not
        if User.objects.filter(username=username).exists():
            return self.create_response(request, {'success': True,
                                                  'message': 'Successfully Registered'})
        else:
            return self.create_response(request, {'success': False,
                                                  'message': 'Failed to Be registered'})

    """
    The function will handle the Login Process
    """
    @xframe_options_exempt
    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post','get'])

        data = self.deserialize(request, request.body,
                                format=request.META.get('CONTENT_TYPE', 'application/json'))

        username = data.get('username', '')
        password = data.get('password', '')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return self.create_response(request, {
                    'success': True,
                })
            else:
                return self.create_response(request, {
                    'success': False,
                    'reason': 'disabled',
                }, HttpForbidden)
        else:
            return self.create_response(request, {
                'success': False,
                'reason': 'incorrect',
            }, HttpUnauthorized)

    def logout(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        if request.user and request.user.is_authenticated():
            logout(request)
            return self.create_response(request, {'success': True})
        else:
            return self.create_response(request, {'success': False}, HttpUnauthorized)


class SchoolResource(ModelResource):
    class Meta:
        queryset = School.objects.all()
        allowed_methods = ['get']
        resource_name = 'school'
        fields = ['id', 'name', 'code']
        authorization = Authorization()
        filtering = {
            'id': ALL,
            'name': ALL,
            'code': ALL,
        }

    def dehydrate(self, bundle):
        bundle.data['total_courses'] = Courses.objects.filter(school=bundle.obj).count()

        return bundle


class YearResource(ModelResource):
    class Meta:
        queryset = Year.objects.all()
        allowed_methods = ['get']
        resource_name = 'year'
        fields = ['id', 'name', 'code', 'is_active']
        authorization = Authorization()
        filtering = {
            'id': ALL,
            'name': ALL,
            'code': ALL,
            'is_active': ALL,
        }

class CourseCategoryResource(ModelResource):
    class Meta:
        queryset = CourseCategory.objects.all()
        allowed_methods = ['get']
        resource_name = 'courseCategory'
        fields = ['id', 'name', 'is_active']
        authorization = Authorization()
        filtering = {
            'id': ALL,
            'name': ALL,
            'is_acctive': ALL,
        }

class CourseLevelResource(ModelResource):
    class Meta:
        queryset = CourseLevel.objects.all()
        allowed_methods = ['get']
        resource_name = 'courseLevel'
        fields = ['id', 'name', 'is_active']
        authorization = Authorization()
        filtering = {
            'id': ALL,
            'name': ALL,
            'is_active': ALL,
        }


class AcademicYearResource(ModelResource):
    class Meta:
        queryset = AcademicYear.objects.all()
        allowed_methods = ['get']
        resource_name = 'academic'
        fields = ['id', 'name', 'is_active']
        authorization = Authorization()
        filtering = {
            'id': ALL,
            'name': ALL,
            'is_active': ALL,
        }

class CourseResource(ModelResource):
    school = fields.ForeignKey(SchoolResource, 'school', null=True, blank=True, full=True)
    category = fields.ForeignKey(CourseCategoryResource, 'category', null=True, blank=True, full=True)
    level = fields.ForeignKey(CourseLevelResource, 'level', null=True, blank=True, full=True)
    academic = fields.ForeignKey(AcademicYearResource, 'academic', null=True, blank=True, full=True)
    class Meta:
        queryset = Courses.objects.all().order_by('-name')
        allowed_methods = ['get']
        resource_name = 'course'
        fields = ['id', 'name', 'code', 'is_active']
        authorization = Authorization()
        filtering = {
            'id': ALL,
            'name': ALL,
            'code': ALL,
            'is_active': ALL,
            'school': ALL_WITH_RELATIONS,
            'category': ALL_WITH_RELATIONS,
            'level': ALL_WITH_RELATIONS,
            'academic': ALL_WITH_RELATIONS,
        }

    def dehydrate(self, bundle):
        bundle.data['total_subjects'] = Subjects.objects.filter(course=bundle.obj).count()

        return bundle



class SubjectResource(ModelResource):
    course = fields.ForeignKey(CourseResource, 'course', null=True, blank=True, full=True)
    year = fields.ForeignKey(YearResource, 'year', null=True, blank=True, full=True)
    academic = fields.ForeignKey(AcademicYearResource, 'academic', null=True, blank=True, full=True)
    class Meta:
        queryset = Subjects.objects.all()
        allowed_methods = ['get']
        resource_name = 'subject'
        fields = ['id', 'name', 'code', 'is_active']
        authorization = Authorization()
        filtering = {
            'id': ALL,
            'name': ALL,
            'code': ALL,
            'is_active': ALL,
            'course': ALL_WITH_RELATIONS,
            'year': ALL_WITH_RELATIONS,
            'academic': ALL_WITH_RELATIONS,
        }

class SchoolLinkerResource(ModelResource):
    school = fields.ForeignKey(SchoolResource, 'school', null=True, blank=True, full=True)
    user = fields.ForeignKey(UserResource, 'user', null=True, blank=True, full=True)
    class Meta:
        queryset = SchoolLinker.objects.all()
        allowed_methods = ['get']
        resource_name = 'linker'
        authorization = Authorization()
        filtering = {
            'id': ALL,
            'school': ALL_WITH_RELATIONS,
            'user': ALL_WITH_RELATIONS,
        }



class DescriptionResource(ModelResource):
    subject = fields.ForeignKey(SubjectResource, 'subject', null=True, blank=True, full=True)
    user = fields.ForeignKey(UserResource, 'user', null=True, blank=True, full=True)
    class Meta:

        queryset = Descriptions.objects.all().order_by('-updated')
        allowed_methods = ['get', 'post']
        resource_name = 'article'
        fields = ['id', 'description', 'updated']
        authorization = Authorization()
        filtering = {
            'id': ALL,
            'description': ALL,
            'updated': ALL,
            'subject': ALL_WITH_RELATIONS,
        }

    def dehydrate(self, bundle):
        bundle.data['total_likes'] = Likes.objects.filter(description=bundle.obj).count()
        bundle.data['total_comments'] = DescriptionsComments.objects.filter(description=bundle.obj).count()
        imagesObj = Images.objects.filter(description=bundle.obj)
        image_counter = 1
        for image in imagesObj:
            bundle.data['image'+str(image_counter)] = str(image.url)
            image_counter += 1
        return bundle

    def authorized_read_list(self, object_list, bundle):
        return object_list.filter(user=bundle.request.user)


class DescriptionCommentResource(ModelResource):
    description = fields.ToOneField(DescriptionResource, 'description', null=True, blank=True, full=True)
    user = fields.ForeignKey(UserResource, 'user', null=True, blank=True, full=True)
    class Meta:
        queryset = DescriptionsComments.objects.all()
        allowed_methods = ['get']
        resource_name = 'comment'
        fields = ['id', 'comment', 'updated']
        authorization = Authorization()
        filtering = {
            'id': ALL,
            'comment': ALL,
            'updated': ALL,
            'description': ALL_WITH_RELATIONS,
            'user': ALL_WITH_RELATIONS,
        }



class LikeResource(ModelResource):
    description = fields.ForeignKey(DescriptionResource, 'description', null=True, blank=True, full=True)
    user = fields.ForeignKey(UserResource, 'user', null=True, blank=True, full=True)
    class Meta:
        queryset = Likes.objects.all()
        allowed_methods = ['get']
        resource_name = 'like'
        authorization = Authorization()
        filtering = {
            'id': ALL,
            'description': ALL_WITH_RELATIONS,
            'user': ALL_WITH_RELATIONS,
        }


class ImageResource(ModelResource):
    description = fields.ForeignKey(DescriptionResource, 'description', null=True, blank=True, full=True)
    class Meta:
        queryset = Images.objects.all()
        allowed_methods = ['get']
        resource_name = 'image'
        fields = ['id', 'url', 'name', 'is_active']
        authorization = Authorization()
        filtering = {
            'id': ALL,
            'name': ALL,
            'is_active': ALL,
            'description': ALL_WITH_RELATIONS,
        }

class UserProfileResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user', null=True, blank=True, full=True)
    school = fields.ForeignKey(SchoolResource, 'school', null=True, blank=True, full=True)
    course = fields.ForeignKey(CourseResource, 'course', null=True, blank=True, full=True)
    year = fields.ForeignKey(YearResource, 'year', null=True, blank=True, full=True)
    academic = fields.ForeignKey(AcademicYearResource, 'academic', null=True, blank=True, full=True)
    class Meta:
        queryset = UserProfile.objects.all()
        allowed_methods = ['get']
        resource_name = 'profile'
        fields = ['id', 'middle_name', 'display']
        authorization = Authorization()
        filtering = {
            'id': ALL,
            'middle_name': ALL,
            'display': ALL,
            'user': ALL_WITH_RELATIONS,
            'school': ALL_WITH_RELATIONS,
            'course': ALL_WITH_RELATIONS,
            'year': ALL_WITH_RELATIONS,
            'academic': ALL_WITH_RELATIONS,
        }


class NotificationResource(ModelResource):
    sender = fields.ForeignKey(UserResource, 'sender', null=True, blank=True, full=True)
    school = fields.ForeignKey(SchoolResource, 'school', null=True, blank=True, full=True)
    course = fields.ForeignKey(CourseResource, 'course', null=True, blank=True, full=True)
    year = fields.ForeignKey(YearResource, 'year')
    class Meta:
        queryset = Notifications.objects.all()
        allowed_methods = ['get']
        resource_name = 'notification'
        fields = ['id', 'registered', 'description']
        authorization = Authorization()
        filtering = {
            'id': ALL,
            'registered': ALL,
            'description': ALL,
            'sender': ALL_WITH_RELATIONS,
            'school': ALL_WITH_RELATIONS,
            'course': ALL_WITH_RELATIONS,
            'year': ALL_WITH_RELATIONS,
        }


class RecoveryResource(ModelResource):
    class Meta:
        queryset = Recovery.objects.all()
        allowed_methods = ['get']
        resource_name = 'recovery'
        fields = ['id', 'phone', 'code', 'waiting']
        authorization = Authorization()
        filtering = {
            'id': ALL,
            'phone': ALL,
            'code': ALL,
            'waiting':  ALL,
        }
