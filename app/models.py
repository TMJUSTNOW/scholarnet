############################################################################
# Author: Daniel Kindimba
# Project: ScholarNet
############################################################################
from django.conf import settings
from django.db import models
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models import Q
import secretballot
import datetime



###################################################################################
# A Class for Creating Database Table for Storing Institues/Schoools
###################################################################################
class School(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False, unique=True)
    code = models.CharField(max_length=50, null=False, blank=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = u'School'
        verbose_name_plural = u'Schools'

    def __str__(self):
        return self.name


####################################################################################
#A class for Creating Table for Storing Study Years
####################################################################################
class Year(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    code = models.CharField(max_length=5, null=False, blank=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = u'Year'
        verbose_name_plural = u'Years'

    def __str__(self):
        return self.name


#####################################################################################
# A class for Creating Course Categories Database Table
#####################################################################################
class CourseCategory(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = u'Course Category'
        verbose_name_plural = u'Courses Categories'

    def __str__(self):
        return self.name


#######################################################################################
# A class for creating the courses Levels
#######################################################################################
class CourseLevel(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = u'Course Level'
        verbose_name_plural = u'Courses Levels'

    def __str__(self):
        return self.name

#####################################################################################
# A Class for Creating Courses Table for Storing Instiutes Courses
######################################################################################
class Courses(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    code = models.CharField(max_length=50, null=True, blank=True)
    school = models.ForeignKey(School)
    course_category = models.ForeignKey(CourseCategory, null=True, blank=True)
    level = models.ForeignKey(CourseLevel, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = u'Course'
        verbose_name_plural = u'Courses'

    def __str__(self):
        return self.name


#######################################################################################################
# A class for Creating the table for storing the Academic Year that are supported
#######################################################################################################
class AcademicYear(models.Model):
    name = models.CharField(max_length=300, null=False, blank=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = u'Academic Year'
        verbose_name_plural = u'Academic Years'

    def __str__(self):
        return self.name

#######################################################################################
# A class For Creating Subjects Table for Storing Institute Course Sujects
#######################################################################################
class Subjects(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    code = models.CharField(max_length=50, null=True, blank=True)
    course = models.ForeignKey(Courses)
    year = models.ForeignKey(Year, null=False, blank=False)
    academic = models.ForeignKey(AcademicYear, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = u'Subject'
        verbose_name_plural = u'Subjects'

    def __str__(self):
        return self.name


##########################################################################################
# A class for creating School Linking Table
##########################################################################################
class SchoolLinker(models.Model):
    school = models.ForeignKey(School)
    user = models.ForeignKey(User)



##########################################################################################
# A class for Creating Descriptions Table for Storing the Instiute Course Subjects Posts
##########################################################################################
class Descriptions(models.Model):
    description = models.TextField(null=False, blank=False)
    subject = models.ForeignKey(Subjects, null=True, blank=True)
    user = models.ForeignKey(User)
    registered = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = u'Description'
        verbose_name_plural = u'Descriptions'


######################################################################################################
# A class for Creating DecriptionsComments Table for Storing Institue Course Subjects Posts Comments
######################################################################################################
class DescriptionsComments(models.Model):
    description = models.ForeignKey(Descriptions)
    comment = models.TextField()
    user = models.ForeignKey(User)
    registered = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

Descriptions.comments = property(lambda u: DescriptionsComments.objects.filter(description=u).count())




######################################################################################################
# A class For Creating Likes Table for Storing Instiute Course Subjects Posts Likes
######################################################################################################
class Likes(models.Model):
    description = models.ForeignKey(Descriptions)
    user = models.ForeignKey(User)

Descriptions.recommend = property(lambda u: Likes.objects.filter(description=u).count())


######################################################################################################
# A Class for Creating Images Table for Storing Institute Course Subjects Posts Images
######################################################################################################
class Images(models.Model):
    url = models.ImageField(upload_to="images/%Y/%m/%d", null=True, blank=True)
    description = models.ForeignKey(Descriptions, null=False, blank=False)
    name = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        try:
            this = Images.objects.get(id=self.id)
            if this.url != self.url:
                this.url.delete()
        except: pass
        super(Images, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u'Image'
        verbose_name_plural = u'Images'


##########################################################################################################
# A class for creating UserProfile Table for Registered user, to Store basic Information of users
###########################################################################################################
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    display = models.CharField(max_length=50, null=False, blank=False)
    school = models.ForeignKey(School, null=True, blank=True)
    year = models.ForeignKey(Year, null=True, blank=True)
    academic = models.ForeignKey(AcademicYear, null=True, blank=True)
    course = models.ForeignKey(Courses, null=True, blank=True)


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


#################################################################################################
# A class for creating Feedback Table for Storing all the User Feedbacks
#################################################################################################
class Feedback(models.Model):
    user = models.ForeignKey(User)
    satisfaction = models.TextField(blank=True, null=True)
    features = models.TextField(blank=True, null=True)
    problems = models.TextField(blank=True, null=True)
    addfeatures = models.TextField(blank=True, null=True)
    registered = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)



####################################################################################################
# A class for creating Notifications table fro storing all the notifications
####################################################################################################
class Notifications(models.Model):
    sender = models.ForeignKey(User)
    registered = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    description = models.TextField()
    school = models.ForeignKey(School)
    course = models.ForeignKey(Courses)


#####################################################################################################
# A class For Temporary Password Recovery code
######################################################################################################
class Recovery(models.Model):
    phone = models.CharField(max_length=15, null=False, blank=False)
    code = models.CharField(max_length=4, null=False, blank=False)
    waiting = models.BooleanField(default=False)

    def __str__(self):
        return self.phone
