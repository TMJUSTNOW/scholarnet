__author__ = 'dpak'

from django import forms
from passwords.fields import PasswordField
from passwords.validators import (
    DictionaryValidator, LengthValidator, ComplexityValidator)
from django.contrib.auth.models import *
from .models import *
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordResetForm



#image Registration form
class ImageForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ['url']


#institute registration form
class SchoolRegistration(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name', 'code']


#Email Validation Form for Recovering the Password
class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email,is_active=True).exists():
            raise ValidationError("There is no user registered with the specified email address!")
        return email

#User Registration form
class registration(forms.ModelForm):
    username = forms.CharField()
    password = PasswordField(validators=[
        ComplexityValidator(complexities=dict(
            DIGITS=1
        )),
    ])
    password1 = PasswordField(validators=[
        ComplexityValidator(complexities=dict(
            DIGITS=1
        )),
    ])
    # field = forms.CharField(validators=[
    #     DictionaryValidator(words=['anal','kuma','mkundu'], threshold=0.9),
    # ])

    class Meta:
        model = User
        fields = ['username', 'password', 'password1']

    def clean(self):
        cleaned_data = super(registration, self).clean()
        if 'password' in self.cleaned_data and 'password1' in self.cleaned_data:
            if self. cleaned_data['password'] != self.cleaned_data['password1']:
                self._errors['password'] = 'Password Must Match'
                self._errors['password1'] = 'Password Must Match'
        if 'username' in self.cleaned_data and 'username1' in self.cleaned_data:
            if self.cleaned_data['username'] != self.cleaned_data['username1']:
                self._errors['username'] = 'Phone Number Must Match'
                self._errors['username1'] = 'Phone Number Must Match'
        if 'username' in self.cleaned_data:
            if self. cleaned_data['username'] and User.objects.filter(username= self.cleaned_data['username']).count() > 0:
                self._errors['username'] = 'This Phone is already registered, Try another'
        return self.cleaned_data

    def save(self, commit=True):
        user = super(registration, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.last_login = timezone.now()
            user.is_active = False
            user.save()
        return user