from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS, Resource
from django.contrib.auth.models import *
from app.models import *



class BaseCorsResource(Resource):
    """
    Class implementing CORS
    """
    def create_response(self, *args, **kwargs):
        response = super(BaseCorsResource, self).create_response(*args, **kwargs)
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    def method_check(self, request, allowed=None):
        if allowed is None:
            allowed = []

        request_method = request.method.lower()
        allows = ','.join(map(str.upper, allowed))

        if request_method == 'options':
            response = HttpResponse(allows)
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Headers'] = 'Content-Type'
            response['Allow'] = allows
            raise ImmediateHttpResponse(response=response)

        if not request_method in allowed:
            response = http.HttpMethodNotAllowed(allows)
            response['Allow'] = allows
            raise ImmediateHttpResponse(response=response)

        return request_method


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        allowed_methods = ['get']
        resource_name = 'user'
        fields = ['id', 'first_name', 'last_name', 'username', 'is_active']
        authorization = Authorization()
        filtering = {
            'id': ALL,
            'username': ALL,
        }



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
        queryset = Courses.objects.all()
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



class SubjectResource(ModelResource):
    course = fields.ForeignKey(CourseResource, 'course', null=True, blank=True, full=False)
    year = fields.ForeignKey(YearResource, 'year', null=True, blank=True, full=True)
    academic = fields.ForeignKey(AcademicYearResource, 'academic', null=True, blank=True, full=True)
    class Meta:
        queryset = Subjects.objects.all()
        allowed_methods = ['get', 'post']
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



class DescriptionResource(BaseCorsResource, ModelResource):
    subject = fields.ForeignKey(SubjectResource, 'subject', null=True, blank=True, full=True)
    user = fields.ForeignKey(UserResource, 'user', null=True, blank=True, full=True)
    class Meta:
        queryset = Descriptions.objects.all()
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


class DescriptionCommentResource(ModelResource):
    description = fields.ForeignKey(DescriptionResource, 'description', null=True, blank=True, full=True)
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
