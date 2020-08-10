from django.shortcuts import render
from firstapp.models import User
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.core import serializers
from django.core.mail import send_mail
import json
import random

# Create your views here.
def checkUsername(request):
    respose={}
    if request.method=="POST":
        Username = request.POST.get('Username')
        user = User.objects.filter(User_name=Username)
        if user:
            respose['Used']=True
        else:
            respose['Used']=False
        return JsonResponse(respose)

def checkEmail(request):
    respose={}
    if request.method=="POST":
        Email = request.POST.get('Email')
        user = User.objects.filter(User_email=Email)
        if user:
            respose['Used']=True
        else:
            respose['Used']=False
        return JsonResponse(respose)

def captcha(request):
    respose={}
    if request.method=="POST":
        Email = request.POST.get('Email')
        number = random.randint(100000,999999)
        try:
            send_mail('金刚石注册验证',"您的验证码为：" + str(number) + "请尽快完成验证",'1205672770@qq.com',[Email])
            respose['Status']=True
            request.session['checknumber']=number
        except Exception as e:
            respose['Status']=False
        return JsonResponse(respose)

def register(request):
    respose={}
    if request.method=="POST":
        Email = request.POST.get('Email')
        Username = request.POST.get('Username')
        Password = request.POST.get('Password')
        Captcha = int(request.POST.get('Captcha'))
        if Captcha==request.session.get('checknumber',default=None):
            new_user = User()
            new_user.password=Password
            new_user.User_email=Email
            new_user.User_name=Username
            new_user.save()
            respose['Status']=True
        else:
            respose['Status']=False
        return JsonResponse(respose)

def login(request):
    respose={}
    if request.method=="POST":
        Email = request.POST.get('Email')
        Password = request.POST.get('Password')
        user = User.objects.filter(User_email=Email).filter(password=Password)
        if user:
            request.session['is_login']=True
            request.session['user_id']=user[0].pk
            respose['Status']=True
        else:
            respose['Status']=False
        return JsonResponse(respose)
