from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from . models import *

# Register your models here.

admin.site.register(School)
admin.site.register(Courses)
admin.site.register(Subjects)
admin.site.register(Year)
admin.site.register(Descriptions)
admin.site.register(Images)
admin.site.register(Recovery)
admin.site.register(CourseCategory)
admin.site.register(CourseLevel)
admin.site.register(AcademicYear)