from collections import UserDict
from dataclasses import fields
from tkinter.tix import TEXT
from turtle import textinput
from typing import Text
from xml.dom import InvalidCharacterErr
from django import forms
from django.contrib.auth.models import User

from catalog.models import profile


error={
      'min_length':'حداقل 5 کلاراکتر وارد کنید',
      'required':'این فیلد اجباری است',
      'invalid':'ایمیل صحیح نیست',
      
      
      
}

class UserRegisterForm(forms.Form):
    user_name=forms.CharField(required=False,max_length=200,error_messages=error, widget=forms.TextInput(attrs={'placeholder':'نام کاربری'})) 
    email=forms.EmailField(required=False,min_length=5,error_messages=error, widget=forms.TextInput(attrs={'placeholder':'ایمیل'}))
    first_name=forms.CharField(required=False,min_length=5,error_messages=error,max_length=200, widget=forms.TextInput(attrs={'placeholder':'نام'}))
    last_name=forms.CharField(required=False,max_length=200,error_messages=error, widget=forms.TextInput(attrs={'placeholder':'نام خانوادگی'}))
    password_1=forms.CharField(required=False,max_length=200,error_messages=error, widget=forms.TextInput(attrs={'placeholder':'رمز'}))
    password_2=forms.CharField(max_length=200,error_messages=error, widget=forms.TextInput(attrs={'placeholder':'تایید رمز'}))


class UserLoginForm(forms.Form):
    user_name=forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder':'  نام کاربری یا ایمیل'})) 
    password_1=forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder':'رمز'}))


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields=['email','first_name','last_name']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model= profile
        fields=['tel','address']

class PhoneForm(forms.Form):
    phone=forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'  شماره تماس'}))

class CodeForm(forms.Form):
    code=forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'  کد دریافتی'}))